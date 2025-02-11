import logging
import pytest
from src.common.util.log import LogHandler

@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("LOG_FILE_PATH", "log/test_app.log")

def test_log_handler_initialization(mock_env_vars):
    log_handler = LogHandler()
    assert log_handler.log_level == "DEBUG"
    assert log_handler.log_file_path == "log/test_app.log"
    assert isinstance(log_handler.logger, logging.Logger)

def test_log_handler_singleton(mock_env_vars):
    log_handler1 = LogHandler()
    log_handler2 = LogHandler()
    assert log_handler1 is log_handler2
