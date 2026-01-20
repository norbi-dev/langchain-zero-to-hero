# langchain-zero

Script collection demonstrating LangChain capabilities with pgvector and PostgreSQL.

## Features

- **Vector Store**: PostgreSQL with pgvector extension
- **Containerization**: Podman (Docker-compatible)
- **LLM**: Ollama integration
- **Embedding**: Local embeddings with Ollama

## Quick Start

### 1. Install Dependencies

```bash
uv sync
```

### 2. Start PostgreSQL with pgvector

```bash
podman-compose up -d
```

See [PODMAN.md](PODMAN.md) for detailed setup instructions.

### 3. Run Examples

```bash
# RAG with vector database
uv run llm_rag_vector_db.py

# Chat with LLM
uv run chat_with_llm.py

# Using memory
uv run llm_using_memory.py

# Call tools
uv run call_tools.py

# Prompt templates
uv run prompt_templates.py
```

## Tech Stack

- **langchain-postgres**: PostgreSQL vector store integration
- **pgvector**: Vector similarity search in PostgreSQL
- **langchain-ollama**: Local LLM and embeddings
- **Podman**: Container runtime

## Database Connection

Default connection string:
```
postgresql+psycopg://langchain:langchain@localhost:5432/langchain
```

