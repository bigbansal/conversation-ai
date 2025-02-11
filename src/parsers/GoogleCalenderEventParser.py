from datetime import datetime
from typing import Dict, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from src.models.ChatModel import ChatModel
from enum import Enum
from src.common.util.log import LogHandler

logger = LogHandler().get_logger()
class Operation(Enum):
    CREATE = "create"
    RETRIEVE = "retrieve"
    UPDATE = "update"
    DELETE = "delete"
class EventDetails(BaseModel):
    """Structured representation of event details"""
    #make operation enum create,retrieve,update,delete
    operation: str = Field(description="Operation type", default=Operation.CREATE)
    summary: str = Field(description="Event title or summary")
    description: Optional[str] = Field(description="Detailed description of the event", default=None)
    start_time: str = Field(description="Start time of the event in ISO 8601 format")
    end_time: str = Field(description="End time of the event in ISO 8601 format")
    attendees: Optional[list] = Field(description="List of attendee email addresses", default=None)


class EventParser:
    def __init__(self):
        """
        Initialize event parser with Ollama

        :param model_name: Name of the Ollama model to use
        """
        self.llm = ChatModel().load_model()

        # Create a prompt template for event parsing
        #update the prompt to include the operation

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are an expert event parsing assistant. 
            Extract structured event details from natural language input.
            
            Rules for parsing:
            1. Always provide a summary, in case of missing summary, use the given input as the summary
            2. Infer start and end times intelligently
            3. Handle relative and absolute time references
            4. If no specific time given, default start_time and endtime to 3 PM today for 1 hour
            5. Provide a description if possible, otherwise leave it empty
            6. Identify the operation type (create, retrieve, update, delete) from the input based on keywords:
               - "create", "add", "book" for creating events
               - "retrieve", "get", or "show" for retrieving events
               - "update", "modify", or "change" for updating events
               - "delete", "remove", or "cancel" for deleting events


            Output MUST be a valid JSON matching the EventDetails schema.
            """),
            ("human", "Parse the following event request: {input}")
        ])

        # Output parser to ensure structured output
        self.output_parser = PydanticOutputParser(pydantic_object=EventDetails)

    def _normalize_time(self, time_str: str) -> str:
        """
        Normalize and convert time strings to ISO 8601 format

        :param time_str: Input time string
        :return: Normalized ISO 8601 time string
        """
        try:
            # Handle various time formats
            formats = [
                "%I:%M %p",  # 3:30 PM
                "%I %p",  # 3 PM
                "%H:%M",  # 15:30
                "%Y-%m-%d %H:%M",  # 2023-07-15 14:30
                "%B %d, %Y at %I:%M %p"  # July 15, 2023 at 2:30 PM
            ]

            for fmt in formats:
                try:
                    parsed_time = datetime.strptime(time_str, fmt)
                    return parsed_time.isoformat()
                except ValueError:
                    continue

            # Fallback to current time if parsing fails
            return datetime.now().isoformat()

        except Exception as e:
            logger.error(f"Time normalization error: {e}")
            return datetime.now().isoformat()

    def parse_event(self, user_input: str) -> Dict:
        """
        Parse event details from natural language input

        :param user_input: Natural language event description
        :return: Structured event details
        """
        try:
            # Create the chain
            chain = self.prompt | self.llm | self.output_parser

            # Invoke the chain to extract event details
            event_details = chain.invoke({"input": user_input})

            # Prepare the event dictionary
            event_data = {
                "operation" : event_details.operation,
                "summary": event_details.summary or user_input,
                "description": event_details.description or "",
                "start_time": event_details.start_time,
                "end_time": event_details.end_time,
                "attendees": event_details.attendees or []
            }

            return {
                "status": "success",
                "event": event_data
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to parse event: {str(e)}",
                "details": str(e)
            }

    def interactive_event_parsing(self):
        """
        Interactive method to parse events from user input
        """
        while True:
            user_input = input("Enter event details (or 'quit' to exit): ")

            if user_input.lower() == 'quit':
                break

            result = self.parse_event(user_input)

            if result['status'] == 'success':
                logger.debug("\nParsed Event Details:")
                for key, value in result['event'].items():
                    logger.info(f"{key.capitalize()}: {value}")
            else:
                logger.error(f"Error: {result['message']}")



# Example usage
#if __name__ == "__main__":
#    parser = EventParser()
#    parser.interactive_event_parsing()