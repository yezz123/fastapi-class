from unittest.mock import patch

import pytest

from fastapi_class import (
    UNKNOWN_SERVER_ERROR_DETAIL,
    ExceptionAbstract,
    FormattedMessageException,
)


@patch("fastapi_class.ExceptionAbstract.__abstractmethods__", set())
def test_abstract_factory_creation__defaults():
    _instance = ExceptionAbstract()
    assert _instance.exceptions[0][0] == 500
    assert _instance.exceptions[0][1] == UNKNOWN_SERVER_ERROR_DETAIL


@pytest.mark.parametrize("keyword_args", ({}, {"some_var": 0}))
def test_formatted_message_factory__non_formattable_string(keyword_args: dict):
    _instance = FormattedMessageException(exceptions=((500, "Test"),))
    assert _instance(keyword_args).detail == "Test"


@pytest.mark.parametrize("arg", ("t", 0, 3.141592, False))
def test_formatted_message_factory__format_string(arg: str | int | float | bool):
    _instance = FormattedMessageException(exceptions=((500, "Test {test}"),))
    assert _instance(**{"test": arg}).detail == f"Test {arg}"
