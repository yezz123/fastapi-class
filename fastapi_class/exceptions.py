from abc import ABC, abstractmethod
from typing import Any, List

from fastapi import HTTPException, status
from pydantic import BaseModel

UNKNOWN_SERVER_ERROR_DETAIL = "Unknown server error"


class ExceptionAbstract(ABC):
    """Abstract class for exception."""

    _DEFAULT_DETAIL_SPECIAL_NAME = "DEFAULT_DETAIL"
    exceptions: List[tuple[int, str]] = []

    def __init__(self, *, exceptions: List[tuple[int, str]] = None) -> None:
        self.exceptions = exceptions or [
            (status.HTTP_500_INTERNAL_SERVER_ERROR, UNKNOWN_SERVER_ERROR_DETAIL)
        ]

    @classmethod
    @abstractmethod
    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        raise NotImplementedError


class FormattedMessageException(BaseModel, ExceptionAbstract):
    """Exception with formatted message."""

    exceptions: List[tuple[int, str]]

    def __call__(self, *_, **kwargs):
        _exception = self.exceptions[0]

        try:
            detail = _exception[1].format(**kwargs)
        except (IndexError, KeyError):
            detail = _exception[1]

        return HTTPException(status_code=_exception[0], detail=detail)
