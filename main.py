import os
import random
import boto3
import urllib.request
from botocore.exceptions import ClientError
import enum
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Enum, func, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from pydantic import BaseModel, ConfigDict

# --- 1. Configuration & AWS Identity ---
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")

if DATABASE_HOST:
    DATABASE_URL = (
        f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}"
        f"@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    )
else:
    DATABASE_URL = "sqlite:///./ticketdesk.db"
    
S3_BUCKET = os.getenv("S3_BUCKET_NAME", "my-local-stub-bucket")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

def get_ec2_instance_id():
    """Fetches the EC2/ECS Instance ID using IMDSv2."""
    try:
        req = urllib.request.Request("http://169.254.169.254/latest/api/token", method="PUT")
        req.add_header("X-aws-ec2-metadata-token-ttl-seconds", "21600")
        token = urllib.request.urlopen(req, timeout=1).read().decode()
        
        req_id = urllib.request.Request("http://169.254.169.254/latest/meta-data/instance-id")
        req_id.add_header("X-aws-ec2-metadata-token", token)
        return urllib.request.urlopen(req_id, timeout=1).read().decode()
    except Exception:
        return f"Local-Node-{random.randint(100, 999)}"

INSTANCE_ID = get_ec2_instance_id()

# --- 2. Production Database Pooling ---
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Real-life AWS RDS configuration
    engine = create_engine(
        DATABASE_URL, 
        pool_pre_ping=True, # Automatically reconnects if RDS drops connection
        pool_size=10,       # Max concurrent DB connections per ECS task
        max_overflow=20
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
os.makedirs("static", exist_ok=True)

# --- 3. Models & Schemas ---
class TicketStatus(str, enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class TicketPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    category = Column(String, index=True)
    priority = Column(Enum(TicketPriority), default=TicketPriority.MEDIUM)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN)
    created_by = Column(String, index=True)
    file_url = Column(String, nullable=True)
    comments = relationship("Comment", back_populates="ticket", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    author = Column(String)
    text = Column(Text)
    ticket = relationship("Ticket", back_populates="comments")

Base.metadata.create_all(bind=engine)

class CommentCreate(BaseModel):
    text: str
    author: str

class CommentResponse(BaseModel):
    id: int
    text: str
    author: str
    model_config = ConfigDict(from_attributes=True)

class TicketCreate(BaseModel):
    title: str
    description: str
    category: str
    priority: TicketPriority
    created_by: str

class TicketStatusUpdate(BaseModel):
    status: TicketStatus

class FileAttachedUpdate(BaseModel):
    file_url: str

class TicketResponse(TicketCreate):
    id: int
    status: TicketStatus
    file_url: Optional[str] = None
    comments: List[CommentResponse] = []
    model_config = ConfigDict(from_attributes=True)

# --- 4. FastAPI & Security Middleware ---
app = FastAPI(title="TicketDesk API")

# Allow Frontend to hit Backend if hosted on different domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-EC2-Instance-Id"]
)

@app.middleware("http")
async def add_instance_id_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-EC2-Instance-Id"] = INSTANCE_ID
    return response

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# Deep ALB Health Check
@app.get("/api/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1")) 
        return {"status": "healthy", "instance_id": INSTANCE_ID, "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Database connection failed")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")

# --- 5. Endpoints ---
@app.post("/api/tickets/", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    db_ticket = Ticket(**ticket.model_dump())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

# Protected via Pagination (skip/limit defaults)
# Replace ONLY the get_tickets function in your main.py with this:

@app.get("/api/tickets/", response_model=List[TicketResponse])
def get_tickets(
    status: Optional[TicketStatus] = None, 
    priority: Optional[TicketPriority] = None,
    category: Optional[str] = None,
    user: Optional[str] = None, 
    skip: int = 0, limit: int = 150, 
    db: Session = Depends(get_db)
):
    query = db.query(Ticket)
    if status: query = query.filter(Ticket.status == status)
    if priority: query = query.filter(Ticket.priority == priority)
    if category: query = query.filter(Ticket.category == category)
    if user and user != "Admin": query = query.filter(Ticket.created_by == user)
    return query.order_by(Ticket.id.desc()).offset(skip).limit(limit).all()


@app.put("/api/tickets/{ticket_id}/status")
def update_status(ticket_id: int, status_update: TicketStatusUpdate, db: Session = Depends(get_db)):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not db_ticket: raise HTTPException(status_code=404, detail="Ticket not found")
    db_ticket.status = status_update.status
    db.commit()
    return {"status": "updated"}

@app.post("/api/tickets/{ticket_id}/comments/")
def add_comment(ticket_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    db_comment = Comment(ticket_id=ticket_id, text=comment.text, author=comment.author)
    db.add(db_comment)
    db.commit()
    return {"status": "added"}

@app.get("/api/tickets/{ticket_id}/presigned-url")
def get_presigned_url(ticket_id: int, filename: str, file_size: Optional[int] = None):
    # Enforce 10MB Limit Server-Side
    MAX_FILE_SIZE = 10 * 1024 * 1024 
    if file_size and file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds the maximum allowed limit of 10MB.")

    s3_key = f"tickets/{ticket_id}/{filename}"
    if S3_BUCKET == "my-local-stub-bucket":
        return {"url": "http://localhost:8000/mock-upload", "key": s3_key}
        
    s3_client = boto3.client('s3', region_name=AWS_REGION)
    try:
        url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': S3_BUCKET, 'Key': s3_key},
            ExpiresIn=3600
        )
        return {"url": url, "key": s3_key}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/tickets/{ticket_id}/attach")
def record_attachment(ticket_id: int, attachment: FileAttachedUpdate, db: Session = Depends(get_db)):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    db_ticket.file_url = attachment.file_url
    db.commit()
    return {"status": "recorded"}

@app.get("/api/dashboard/")
def get_dashboard(user: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Ticket.status, func.count(Ticket.id)).group_by(Ticket.status)
    if user and user != "Admin": query = query.filter(Ticket.created_by == user)
    status_counts = dict(query.all())
    return {"status_counts": {s.value: status_counts.get(s, 0) for s in TicketStatus}}
