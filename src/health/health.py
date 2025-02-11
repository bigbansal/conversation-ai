import src.common.service
from src.common.util.log import LogHandler
from src.common.util.decorator import log_transaction
logger = LogHandler().get_logger()


@log_transaction
def health_check():
    logger.info("Health check")
    return "OK"

@log_transaction
def clear_up():
    for service in src.common.service.services:
        try:
            service.close()
        except Exception as e:
            logger.error(f"Error closing service {service}: {str(e)}", exc_info=True)