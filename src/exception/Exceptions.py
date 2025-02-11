# File: src/exception/Exceptions.py
from .ExceptionEnum import ExceptionEnum

class CustomException(Exception):
    """Base class for other exceptions"""
    def __init__(self, exception_enum: ExceptionEnum):
        self.status_code = exception_enum.status_code
        self.error_code = exception_enum.error_code
        self.message = exception_enum.message
        super().__init__(self.message)

class NotFoundException(CustomException):
    """Raised when a resource is not found"""
    def __init__(self):
        super().__init__(ExceptionEnum.NOT_FOUND)

class BadRequestException(CustomException):
    """Raised when a bad request is made"""
    def __init__(self):
        super().__init__(ExceptionEnum.BAD_REQUEST)

class UnauthorizedException(CustomException):
    """Raised when a request is unauthorized"""
    def __init__(self):
        super().__init__(ExceptionEnum.UNAUTHORIZED)

class InternalServerError(CustomException):
    """Raised when a request is unauthorized"""
    def __init__(self):
        super().__init__(ExceptionEnum.UNAUTHORIZED)
