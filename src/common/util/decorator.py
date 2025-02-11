import functools
import inspect
import logging

from src.common.util.log import LogHandler

# Initialize logger
logger = LogHandler().get_logger()

def log_transaction(func=None, message = None, level = logging.INFO):
    if func is None:
        return functools.partial(log_transaction, message=message, level=level)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.log(level, "BEGIN: %s called with args: %s, kwargs: %s", message or func.__name__, args, kwargs)
            return_value = func(*args, **kwargs)
            logger.log(level, "END: %s returned: %s", message or func.__name__, return_value)
        except Exception as e:
            logger.error("Error in %s: %s", func.__name__, str(e), exc_info=True)
            raise
        return return_value

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            logger.log(level, f"BEGIN: {message or func.__name__} called with args: {args}, kwargs: {kwargs}")
            return_value = await func(*args, **kwargs)
            logger.log(level, f"END: {message or func.__name__} returned: {return_value}")
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}" ,exc_info=True)
            raise
        return return_value

    if inspect.iscoroutinefunction(func):
        return async_wrapper
    return wrapper