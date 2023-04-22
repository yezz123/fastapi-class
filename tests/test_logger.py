import pytest

from fastapi_class import logger


@pytest.fixture
def setup_logger():
    return logger


def test_logger_disable(setup_logger):
    logger = setup_logger
    logger.disabled = True
