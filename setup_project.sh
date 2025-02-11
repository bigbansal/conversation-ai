#!/bin/bash

# Set project name
project_name="conversation-ai"

# Create project directory
mkdir $project_name
cd $project_name

# Create directories
mkdir -p .devcontainer
mkdir -p .github/workflows
mkdir -p .vscode
mkdir -p src
mkdir -p src/common/util
mkdir -p src/exception
mkdir -p src/models
mkdir -p src/parsers
mkdir -p src/thirdparty/google
mkdir -p tests

# Create __init__.py files
touch src/__init__.py
touch src/common/__init__.py
touch src/common/util/__init__.py
touch src/exception/__init__.py
touch src/models/__init__.py
touch src/parsers/__init__.py
touch src/thirdparty/__init__.py
touch src/thirdparty/google/__init__.py
touch tests/__init__.py

echo "Project structure created successfully."
