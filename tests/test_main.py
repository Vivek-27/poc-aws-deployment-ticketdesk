import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

# Import your FastAPI app and database components
from main import app, Base, get_db

# ---------------------------------------------------------
# 1. Test Database Setup (In-Memory SQLite)
# ---------------------------------------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency so the app uses the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# ---------------------------------------------------------
# 2. Pytest Fixture to Reset DB Before Each Test
# ---------------------------------------------------------
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# ---------------------------------------------------------
# 3. Unit Tests
# ---------------------------------------------------------
def test_health_check():
    """Verify the health check endpoint returns 200 and healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "instance_id" in response.json()

def test_create_ticket():
    """Verify a ticket can be created and returns the correct data."""
    payload = {
        "title": "VPN Issue",
        "description": "Cannot connect to the office VPN.",
        "category": "Network",
        "priority": "HIGH",
        "created_by": "Employee A"
    }
    response = client.post("/api/tickets/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "VPN Issue"
    assert data["status"] == "OPEN"
    assert "id" in data

def test_get_tickets():
    """Verify we can fetch the list of tickets."""
    # First, inject a ticket
    client.post("/api/tickets/", json={
        "title": "Mouse broken",
        "description": "Scroll wheel is stuck.",
        "category": "Hardware",
        "priority": "LOW",
        "created_by": "Employee B"
    })
    
    response = client.get("/api/tickets/")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    assert data[0]["title"] == "Mouse broken"

def test_update_ticket_status():
    """Verify the status of a ticket can be updated."""
    # Create the ticket
    create_res = client.post("/api/tickets/", json={
        "title": "Server down",
        "description": "Production server is unreachable.",
        "category": "Network",
        "priority": "CRITICAL",
        "created_by": "Admin"
    })
    ticket_id = create_res.json()["id"]
    
    # Update status to IN_PROGRESS
    update_res = client.put(f"/api/tickets/{ticket_id}/status", json={"status": "IN_PROGRESS"})
    assert update_res.status_code == 200
    
    # Fetch it back and check the status
    get_res = client.get(f"/api/tickets/?user=Admin")
    ticket = next((t for t in get_res.json() if t["id"] == ticket_id), None)
    
    assert ticket is not None
    assert ticket["status"] == "IN_PROGRESS"
