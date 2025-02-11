import pytest
import logging
from pytest_mock import MockerFixture
from src.common.util.decorator import log_transaction

# Sample function to be decorated
@log_transaction
def sample_function(a, b):
    return a + b

# Sample async function to be decorated
@log_transaction
async def sample_async_function(a, b):
    return a + b

def test_log_transaction_sync(mocker: MockerFixture):
    mock_logger = mocker.patch('src.common.util.log.LogHandler.get_logger')
    mock_logger_instance = mock_logger.return_value
    mock_logger_instance.setLevel(logging.INFO)
    # Ensure the logger is configured to handle INFO level messages
    logging.basicConfig(level=logging.INFO)


    result = sample_function(1, 2)
    assert result == 3

@pytest.mark.asyncio
async def test_log_transaction_async(mocker: MockerFixture):
    mock_logger = mocker.patch('src.common.util.log.LogHandler.get_logger')
    mock_logger_instance = mock_logger.return_value

    result = await sample_async_function(1, 2)
    assert result == 3

    mock_logger_instance.log.assert_any_call(logging.INFO, "BEGIN: sample_async_function called with args: (1, 2), kwargs: {}")
    mock_logger_instance.log.assert_any_call(logging.INFO, "END: sample_async_function returned: 3")

def test_log_transaction_exception(mocker: MockerFixture):
    @log_transaction
    def error_function():
        raise ValueError("An error occurred")

    mock_logger = mocker.patch('src.common.util.log.LogHandler.get_logger')

    with pytest.raises(ValueError, match="An error occurred"):
        error_function()

