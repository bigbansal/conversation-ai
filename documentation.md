# Project Documentation

## Overview
This project uses FastAPI to create an API that interacts with a language model and Google Calendar.

## Endpoints

### GET /
Returns a simple greeting.

### POST /chat
Generates text based on a prompt.

#### Parameters
- `prompt` (str): The input prompt for the model.

#### Response
- `response` (str): The generated text.

### POST /calenderEvent
Handles calendar events by creating, updating, deleting, or listing events in Google Calendar.

#### Parameters
- `prompt` (str): The input prompt containing event details and operation type.

#### Response
- `response` (dict): The result of the calendar operation.

## Setup

### Prerequisites
- Python
- pip

### Installation

1. Install the package using `setup.py`:
    ```bash
    pip install .
    ```

2. Alternatively, install dependencies using `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the environment variables in a `.env` file:
    ```
    MODEL_NAME=your_model_name
    LOG_LEVEL=INFO
    LOG_FILE_PATH=app.log
    ```

4. Run the FastAPI application:
    ```bash
    uvicorn src.api:app --reload
    ```

## Testing
Run the tests using pytest:
```bash
pytest