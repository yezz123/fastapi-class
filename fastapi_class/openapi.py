import logging
from collections.abc import Callable, Iterable

from fastapi import HTTPException, status
from pydantic import BaseModel, Field

logger = logging.getLogger("fastapi_class")


class ExceptionModel(BaseModel):
    """Exception model."""

    detail: str = Field(..., description="Exception details.")


def _exceptions_to_responses(
    exceptions: Iterable[HTTPException | Callable[..., HTTPException]],
):
    """
    Convert exceptions to responses.

    :param exceptions: exceptions
    :return: responses

    :raise TypeError: if exception is not an instance of HTTPException or a factory function

    :example:
    >>> from fastapi import HTTPException, status
    >>> from fastapi_class import _exceptions_to_responses
    >>> _exceptions_to_responses([HTTPException(status.HTTP_400_BAD_REQUEST, detail="Bad request")])

    Results:

    `{400: {'description': 'Bad request', 'model': <class 'fastapi_class.exceptions.ExceptionModel'>}}`
    """
    mapping = {}

    for exception in exceptions:
        try:
            exc = exception if isinstance(exception, HTTPException) else exception()
        except TypeError:
            logger.warning(
                "Exception %s was failed to be parsed. Make sure it's either an HTTPException instance or it's a factory function with arguments having default values."
            )
            exc = HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(exception))
        if exc.status_code not in mapping:
            mapping[exc.status_code] = {
                "description": exc.detail,
                "model": ExceptionModel,
            }
        else:
            mapping[exc.status_code]["description"] += f" or {exc.detail}"

    return mapping
