# Project Name

## Description
A short description of the project.

### Features
- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.6+.
- **Uvicorn**: A lightning-fast ASGI server implementation, using `uvloop` and `httptools`.
- **LangChain**: A framework for developing applications powered by language models.
- **Ollama Llama3.1**: Integration with the Ollama Llama3.1 model for text generation.
- **Docker**: Containerized environment for consistent development and deployment.
- **GitHub Actions**: CI/CD pipeline for automated testing and linting.
- **Environment Configuration**: Separate environment configurations for development, UAT, and production.

## Setup

### Prerequisites
- Docker
- Docker Compose

### Clone the Repository
1. Clone the repository:
    ```bash
    git clone https://github.com/bigbansal/conversation-ai.git
    cd project_name
    ```

### Environment Configuration
1. Create environment-specific `.env` files in the `env` directory. You can use the provided `.env.dev`, `.env.uat`, and `.env.prod` files as templates:

    ```plaintext
    MODEL_NAME=llama3.2
    OS_NAME=linux
    ```

2. Set the `ENV` environment variable to specify the environment (`dev`, `uat`, or `prod`):

    ```bash
    export ENV=dev  # or uat, prod
    ```

### Build and Run the Docker Container
1. Build the Docker image:
    ```bash
    docker build -t conversation-ai .
    ```

2. Run the Docker container:
    ```bash
    docker run -it -p 8000:8000 -e ENV=$ENV conversation-ai
    ```

### Running Locally with Uvicorn
1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the setup script:
    ```bash
    export ENV=dev  # or uat, prod
    ./env/setup_infra.sh
    ```

3. Start the Uvicorn server:
    ```bash
    uvicorn src.api:app --host 0.0.0.0 --port 8000 --env-file ./env/.env.$ENV
    ```

## Running Tests
To run tests, use the following command:
```bash
pytest tests/
```

## Lint Checks
To run lint checks, use the following command:
```bash
pylint src/
```

## Run Tests with coverage
To generate a coverage report, use the following command:
```bash
pytest --cov=src/ tests/
```
## Generate Coverage Report
To generate a coverage report, use the following command:
```bash
coverage report
```
# Generate HTML Report
To generate an HTML coverage report, use the following command:
```bash
coverage html
```
# Open HTML Report
To open the HTML coverage report in a browser, use the following command:
```bash
open htmlcov/index.html  # For macOS
xdg-open htmlcov/index.html  # For Linux
start htmlcov/index.html  # For Windows
```

