FROM docker.io/library/postgres:17

# Install pgvector extension
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    git \
    postgresql-server-dev-17 && \
    cd /tmp && \
    git clone --branch v0.8.1 https://github.com/pgvector/pgvector.git && \
    cd pgvector && \
    make && \
    make install && \
    cd / && \
    rm -rf /tmp/pgvector && \
    apt-get remove -y build-essential git postgresql-server-dev-17 && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV POSTGRES_DB=langchain
ENV POSTGRES_USER=langchain
ENV POSTGRES_PASSWORD=langchain

# Initialize database with pgvector extension
COPY init-db.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
