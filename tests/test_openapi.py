import pytest
from fastapi import HTTPException

from fastapi_class import ExceptionModel, _exceptions_to_responses


def test_exceptions_to_responses__exception():
    assert _exceptions_to_responses({HTTPException(400, "test")}) == {
        400: {"description": "test", "model": ExceptionModel}
    }


def test_exceptions_to_responses__function_exception_factory():
    assert _exceptions_to_responses({lambda: HTTPException(400, "test")}) == {
        400: {"description": "test", "model": ExceptionModel}
    }


def test_exceptions_to_responses__mixed():
    assert _exceptions_to_responses(
        {lambda: HTTPException(404, "test"), HTTPException(400, "test1")}
    ) == {
        400: {"description": "test1", "model": ExceptionModel},
        404: {"description": "test", "model": ExceptionModel},
    }


def test_exceptions_to_responses__collision_on_status_code():
    assert _exceptions_to_responses(
        [lambda: HTTPException(400, "lambda"), HTTPException(400, "exc")]
    ) == {
        400: {"description": "lambda or exc", "model": ExceptionModel},
    }


def test_exceptions_to_response__broad_exception():
    assert _exceptions_to_responses({Exception()}) == {
        400: {"description": "", "model": ExceptionModel}
    }


@pytest.mark.parametrize("data", ("test", 5, 3.14, (1, 2, 3)))
def test_exception_to_response__random_data(data):
    assert _exceptions_to_responses({data}) == {
        400: {"description": str(data), "model": ExceptionModel}
    }
