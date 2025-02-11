# Project Tasks

## Project Setup
- [ ] Create project directory structure
- [ ] Create `__init__.py` files in all directories
- [ ] Create `README.md` with project description and setup instructions
- [ ] Create `.gitignore` file
- [ ] Create `Dockerfile` for containerization
- [ ] Create `.devcontainer/devcontainer.json` for VS Code development container
- [ ] Create GitHub Actions workflow for CI (`.github/workflows/ci.yml`)
- [ ] Create `.vscode/launch.json` for VS Code debugging configuration
- [ ] Create `requirements.txt` for project dependencies
- [ ] Create `setup.py` for packaging
- [ ] Create `pylint.rc` for linting configuration
- [ ] Create `.coveragerc` for coverage configuration
- [ ] Create `.env` file for environment variables

## Code Implementation
- [ ] Implement `CustomException` class and its subclasses in `src/exception/Exceptions.py`
- [ ] Implement FastAPI application in `src/api.py`
- [ ] Implement `EventParser` class in `src/parsers/GoogleCalenderEventParser.py`
- [ ] Implement `ChatModel` class in `src/models/ChatModel.py`
- [ ] Implement logging utility in `src/common/util/log.py`
- [ ] Implement decorator utility in `src/common/util/decorator.py`
- [ ] Implement Google Calendar Manager in `src/thirdparty/google/GoogleCalendarManager.py`

## Testing
- [ ] Create test directory structure
- [ ] Create sample test file `tests/test_sample.py`
- [ ] Write unit tests for `CustomException` classes
- [ ] Write unit tests for FastAPI endpoints
- [ ] Write unit tests for `EventParser` class
- [ ] Write unit tests for `ChatModel` class
- [ ] Write integration tests for Google Calendar Manager

## Documentation
- [ ] Document project setup and usage in `README.md`
- [ ] Document API endpoints in `README.md` or a separate file
- [ ] Document exception handling and error codes
- [ ] Document event parsing rules and examples

## Additional Tasks
- [ ] Ensure Docker container has `llama3.2` or `deepseek` models installed manually
- [ ] Set up environment variables for different environments (dev, uat, prod)
- [ ] Configure Uvicorn server for local development
- [ ] Set up lint checks and coverage reports
