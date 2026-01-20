# Podman Setup Guide

This project uses Podman as the primary containerization engine for running PostgreSQL with pgvector.

## Prerequisites

Install Podman:
- **macOS**: `brew install podman`
- **Linux**: `sudo apt install podman` or `sudo dnf install podman`
- **Windows**: Download from [Podman Desktop](https://podman-desktop.io/)

## Quick Start

### 1. Start PostgreSQL with pgvector

Using podman-compose:
```bash
podman-compose up -d
```

Or using podman directly:
```bash
# Build the image
podman build -t langchain-postgres .

# Run the container
podman run -d \
  --name langchain-postgres \
  -p 5432:5432 \
  -e POSTGRES_DB=langchain \
  -e POSTGRES_USER=langchain \
  -e POSTGRES_PASSWORD=langchain \
  -v pgdata:/var/lib/postgresql/data \
  langchain-postgres
```

### 2. Verify pgvector Installation

```bash
podman exec -it langchain-postgres psql -U langchain -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### 3. Check Container Status

```bash
podman ps
podman logs langchain-postgres
```

### 4. Stop and Remove

```bash
# Using compose
podman-compose down

# Or manually
podman stop langchain-postgres
podman rm langchain-postgres
```

## Docker Compatibility

All commands work with Docker by replacing `podman` with `docker`:
```bash
docker-compose up -d
docker build -t langchain-postgres .
```

## Connection String

The default connection string used in the application:
```
postgresql+psycopg://langchain:langchain@localhost:5432/langchain
```

## Volume Management

List volumes:
```bash
podman volume ls
```

Remove volume (deletes all data):
```bash
podman volume rm pgdata
```
