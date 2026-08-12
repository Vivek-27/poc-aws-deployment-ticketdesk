# ==========================================
# STAGE 1: Builder
# ==========================================
FROM python:3.11-slim as builder
WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ==========================================
# STAGE 2: Runner
# ==========================================
FROM python:3.11-slim

# 1. Create the non-root user FIRST
RUN useradd -m appuser

WORKDIR /app

# 2. Copy virtual environment
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 3. Copy application files and grant ownership to appuser IMMEDIATELY
COPY --chown=appuser:appuser . /app/

# 4. Explicitly create the static folder and ensure the whole /app directory is writable
RUN mkdir -p /app/static && chown -R appuser:appuser /app

# 5. Switch to the non-root user
USER appuser

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
