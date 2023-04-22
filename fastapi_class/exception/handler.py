from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any

from fastapi import HTTPException, status

UNKOWN_SERVER_ERROR_DETAIL = "Unknown server error"


class ExceptionAbstract(ABC):
    _DEFAULT_DETAIL_SPECIAL_NAME = "__detail__"

    def __init__(self, *, exceptions: Iterable[tuple[int, str]] | None = None) -> None:
        self._exceptions = exceptions or [
            (status.HTTP_500_INTERNAL_SERVER_ERROR, UNKOWN_SERVER_ERROR_DETAIL)
        ]

    @classmethod
    @abstractmethod
    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        raise NotImplementedError


class FormattedMessageException(ExceptionAbstract):
    def __call__(self, *_, **kwargs):
        _exception = self._exceptions[0]

        try:
            detail = _exception[1].format(**kwargs)
        except (IndexError, KeyError):
            detail = _exception[1]
        return HTTPException(status_code=_exception[0], detail=detail)
