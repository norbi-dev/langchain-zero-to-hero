FROM postgres:17-alpine

# Install pgvector extension
RUN apk add --no-cache \
    build-base \
    git \
    postgresql-dev && \
    cd /tmp && \
    git clone --branch v0.9.0 https://github.com/pgvector/pgvector.git && \
    cd pgvector && \
    make && \
    make install && \
    cd / && \
    rm -rf /tmp/pgvector && \
    apk del build-base git

# Set environment variables
ENV POSTGRES_DB=langchain
ENV POSTGRES_USER=langchain
ENV POSTGRES_PASSWORD=langchain

# Initialize database with pgvector extension
COPY init-db.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
