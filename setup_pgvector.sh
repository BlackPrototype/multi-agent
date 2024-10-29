#!/bin/bash

set -e

DB_NAME="codebase"
PG_VECTOR_REPO="https://github.com/pgvector/pgvector.git"

echo "Installing PostgreSQL and development libraries..."
sudo apt update
sudo apt install -y postgresql-server-dev-all git make gcc

echo "Installing pgvector extension..."
git clone $PG_VECTOR_REPO
cd pgvector
make
sudo make install

echo "Creating database '$DB_NAME' and enabling pgvector extension..."
sudo su - postgres -c "psql -c 'CREATE DATABASE $DB_NAME;'"
sudo su - postgres -c "psql -d $DB_NAME -c 'CREATE EXTENSION IF NOT EXISTS vector;'"

echo "Creating tables..."
sudo su - postgres -c "psql -d $DB_NAME -c '
CREATE TABLE projects (
     id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
     name VARCHAR(255) NOT NULL,
     github_url TEXT NOT NULL,
     owner VARCHAR(255) NOT NULL,
     repo_name VARCHAR(255) NOT NULL,
     auth0_id VARCHAR(255) NOT NULL,
     files_processed INTEGER NOT NULL
 );

 CREATE TABLE vectors (
     id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
     project_id UUID NOT NULL,
     file_path TEXT NOT NULL,
     vector FLOAT[] NOT NULL,
     FOREIGN KEY (project_id) REFERENCES projects(id)
 );'
"

echo "PostgreSQL setup complete with pgvector and required tables."