from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from .models.Requests import TextPromptRequest
from .models.ChatModel import ChatModel
from src.parsers.GoogleCalenderEventParser import EventParser
from src.common.util.log import LogHandler
from src.common.util.decorator import log_transaction
from src.thirdparty.google.GoogleCalendarManager import GoogleCalendarManager
from middleware.Interceptor import app
from src.exception.Exceptions import (NotFoundException, BadRequestException,
                                      UnauthorizedException, CustomException, InternalServerError)

logger = LogHandler().get_logger()

load_dotenv()


@app.get("/")
def read_root():
    return {"Hello": "World"}
@app.post("/chat")
def chat(prompt: TextPromptRequest):
    try:
        response = ChatModel().invoke(prompt.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@log_transaction()
@app.post("/calenderEvent")
def calenderEvent(prompt: TextPromptRequest):
    try:
        parser = EventParser()
        response = parser.parse_event(prompt.prompt)

        if response['status'] == 'success':
            logger.debug("\nParsed Event Details:")
            #add logic to check if Operation is create, update or delete or list and call the respective function from GoogleCalendarManager
            for key, value in response['event'].items():
                logger.info(f"{key.capitalize()}: {value}")
            google_response = GoogleCalendarManager().performOperation(response)

            if google_response['status'] == 'success':
                logger.debug(f"Success Google Response: {google_response}" )
            else:
                logger.error(f"Error Google Response: {google_response}")

            for key, value in google_response.items():
                logger.info(f"{key.capitalize()}: {value}")
        else:
            logger.error(f"Error: {response['message']}")

        return {"response": response}
    except CustomException as e:
        raise HTTPException(status_code=e.status_code, detail={"error_code": e.error_code, "message": e.message})
    except Exception as e:
        raise HTTPException(status_code=InternalServerError.status_code , detail={"error_code": InternalServerError.error_code, "message": str(e)})

