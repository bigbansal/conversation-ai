from enum import Enum

class ExceptionEnum(Enum):
    NOT_FOUND = (404, "NOT_FOUND", "Resource not found")
    BAD_REQUEST = (400, "BAD_REQUEST", "Bad request")
    UNAUTHORIZED = (403, "UNAUTHORIZED", "Unauthorized access")
    INTERNAL_SERVER_ERROR = (500, "INTERNAL_SERVER_ERROR", "Internal Server Error")

    def __init__(self, status_code, error_code, message):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
