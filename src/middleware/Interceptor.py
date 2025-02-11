from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.common.util.log import LogHandler

logger = LogHandler().get_logger()

class RequestResponseLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log the request
        logger.debug(f"Request: {request.method} {request.url}")
        logger.debug(f"Headers: {request.headers}")
        logger.debug(f"Body: {await request.body()}")

        # Process the request
        response = await call_next(request)

        # Log the response
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        response_body = [section async for section in response.body_iterator]
        logger.debug(f"Response body: {response_body}")

        # Reconstruct the response using an async generator
        async def response_body_generator():
            for section in response_body:
                yield section

        response.body_iterator = response_body_generator()
        return response

app = FastAPI()

# Add the middleware to the application
app.add_middleware(RequestResponseLoggingMiddleware)
