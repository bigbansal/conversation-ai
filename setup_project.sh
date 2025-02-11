#!/bin/bash

# Set project name
converstation-ai="converstation-ai"

# Create project directory
mkdir $converstation-ai
cd $converstation-ai

# Create directories
mkdir -p .devcontainer
mkdir -p .github/workflows
mkdir -p .vscode
mkdir -p src
mkdir -p tests

# Create files with content
cat <<EOL > README.md
# Project Name

## Description
A short description of the project.

## Setup
1. Clone the repository.
    \`\`\`bash
    git clone https://github.com/yourusername/converstation-ai.git
    cd converstation-ai
    \`\`\`
2. Build the Docker image.
    \`\`\`bash
    docker build -t converstation-ai .
    \`\`\`
3. Run the Docker container.
    \`\`\`bash
    docker run -it converstation-ai
    \`\`\`

## Running Tests
To run tests, use the following command:
\`\`\`bash
pytest tests/
\`\`\`
EOL

cat <<EOL > .gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyderworkspace

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/
EOL

cat <<EOL > Dockerfile
# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the application
CMD ["python", "src/main.py"]
EOL

cat <<EOL > .devcontainer/devcontainer.json
{
    "name": "Python 3",
    "dockerFile": "../Dockerfile",
    "settings": {
        "python.pythonPath": "/usr/local/bin/python"
    },
    "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance"
    ],
    "postCreateCommand": "pip install -r requirements.txt"
}
EOL

cat <<EOL > .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Lint with pylint
      run: |
        pip install pylint
        pylint src/

    - name: Test with pytest
      run: |
        pip install pytest
        pytest tests/
EOL

cat <<EOL > .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "\${file}",
            "console": "integratedTerminal"
        }
    ]
}
EOL

cat <<EOL > requirements.txt
# Add your project dependencies here
pylint
pytest
python-dotenv
ollama==0.1.0
EOL

cat <<EOL > setup.py
from setuptools import setup, find_packages

setup(
    name="converstation-ai",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # Add your project dependencies here
    ],
    entry_points={
        'console_scripts': [
            'converstation-ai=src.main:main',
        ],
    },
)
EOL

cat <<EOL > pylint.rc
[MASTER]
ignore=CVS
jobs=1

[MESSAGES CONTROL]
disable=missing-docstring,
        invalid-name,
        line-too-long

[REPORTS]
output-format=colorized
reports=no

[FORMAT]
max-line-length=88
EOL

cat <<EOL > .coveragerc
[run]
branch = True
source =
    src

[report]
show_missing = True
EOL

cat <<EOL > .env
MODEL_NAME=deepeek
EOL

cat <<EOL > src/__init__.py
# Initialize the package
EOL

cat <<EOL > tests/__init__.py
# Initialize the test package
EOL

cat <<EOL > tests/test_sample.py
def test_sample():
    assert True
EOL

cat <<EOL > src/main.py
import os
from dotenv import load_dotenv
import ollama

def load_model():
    load_dotenv()
    model_name = os.getenv("MODEL_NAME")
    if model_name:
        model = ollama.Model(model_name)
        print(f"Loaded model: {model_name}")
        return model
    else:
        raise ValueError("MODEL_NAME not set in .env file")

def main():
    model = load_model()
    # Add your main application logic here

if __name__ == "__main__":
    main()
EOL

echo "Project structure created successfully."