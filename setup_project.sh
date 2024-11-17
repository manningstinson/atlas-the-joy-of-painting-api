#!/bin/bash

# Project name
PROJECT_NAME="atlas-the-joy-of-painting-api"

# Create the main project directory
echo "Creating project directory: $PROJECT_NAME"
mkdir -p $PROJECT_NAME

# Navigate into the project directory
cd $PROJECT_NAME

# Create main files
echo "Creating main project files..."
touch README.md requirements.txt .gitignore config.py

# Create subdirectories and files
echo "Creating subdirectories and files..."

# database directory
mkdir -p database
touch database/__init__.py database/schema.sql database/connection.py

# etl directory
mkdir -p etl
touch etl/__init__.py etl/extract.py etl/transform.py etl/load.py etl/run_etl.py

# data directory with raw and processed subdirectories
mkdir -p data/raw data/processed
touch data/raw/episodes.csv data/raw/colors.csv data/raw/subjects.csv

# api directory
mkdir -p api
touch api/__init__.py api/routes.py api/models.py api/utils.py

# tests directory
mkdir -p tests
touch tests/__init__.py tests/test_api.py tests/test_database.py tests/test_etl.py

# docs directory
mkdir -p docs
touch docs/api_documentation.md docs/database_design.md

# Create the UML diagrams directory
mkdir -p docs/uml_diagrams

echo "Project setup complete!"
