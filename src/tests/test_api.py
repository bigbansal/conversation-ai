import sys
import os
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from pytest_mock import MockerFixture
import logging

# Add the src directory to the sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from src.api import app

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = TestClient(app)

class TestAPI:
    def test_read_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}

    def test_chat(self, mocker: MockerFixture):
        mock_invoke = mocker.patch('src.models.ChatModel.ChatModel.invoke')
        mock_invoke.return_value = "I am fine, thank you!"
        response = client.post("/chat", json={"prompt": "Hello, how are you?"})
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response JSON: {response.json()}")

        assert response.status_code == 200
        assert "response" in response.json()

    def test_calenderEvent(self, mocker: MockerFixture):
        mock_get_calendar_service = mocker.patch(
            'src.thirdparty.google.GoogleCalendarManager.GoogleCalendarManager.get_calendar_service')
        mock_parse_event = mocker.patch('src.parsers.GoogleCalenderEventParser.EventParser.parse_event')
        mock_perform_operation = mocker.patch(
            'src.thirdparty.google.GoogleCalendarManager.GoogleCalendarManager.performOperation')

        # Mock the return value of get_calendar_service
        mock_get_calendar_service.return_value = MagicMock()
        # Mock the return value of parse_event
        mock_parse_event.return_value = {
            "status": "success",
            "event": {
                "summary": "appointment",
                "start_time": "2024-03-15T15:00:00+05:30",
                "end_time": "2024-03-15T16:00:00+05:30",
                "operation": "create"
            }
        }
        # Mock the return value of perform_operation
        mock_perform_operation.return_value = {
            "status": "success",
            "event": {
                "summary": "appointment",
                "start_time": "2024-03-15T15:00:00+05:30",
                "end_time": "2024-03-15T16:00:00+05:30",
                "operation": "create"
            }
        }

        response = client.post("/calenderEvent", json={"prompt": "Create a meeting with John at 10 am tomorrow for 20 minutes"})
        assert response.status_code == 200
        assert "response" in response.json()
        assert "status" in response.json()["response"]
        assert response.json()["response"]["status"] == "success"
        assert "event" in response.json()["response"]
        assert "summary" in response.json()["response"]["event"]
        assert "start_time" in response.json()["response"]["event"]
        assert "end_time" in response.json()["response"]["event"]
        assert "operation" in response.json()["response"]["event"]
        assert response.json()["response"]["event"]["operation"] == "create"