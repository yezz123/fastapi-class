from __future__ import annotations

import functools
from functools import lru_cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import ErrorDetails

Model: dict[str, type[ErrorDetails]] = {}


def register_for_exc(exc: type[Exception]):
    """
    Decorator to register a model for a specific exception.

    :param exc: The exception to register the model for.
    :return: The decorated class.
    """

    def wrapper(cls: type[ErrorDetails]) -> type[ErrorDetails]:
        Model[exc.__name__] = cls
        return cls

    return wrapper


@lru_cache(maxsize=128, typed=True)
def find_model_for_exc(exc: str) -> type[ErrorDetails] | None:
    """
    Find the model for a specific exception.

    :param exc: The exception to find the model for.
    :return: The model for the exception.
    """
    return next((m for e, m in Model.items() if exc == e), None)


@functools.lru_cache(maxsize=64, typed=True)
def errors(*status: int):
    """
    Decorator to register a model for a specific status code.

    :param status: The status code to register the model for.
    :return: The decorated class.
    """
    from .models import ErrorDetails

    models_by_status = {m.get_status(): m for m in Model.values()}
    models = {}
    for status in status:
        model = models_by_status.get(status, ErrorDetails)
        models[status] = {"model": model}
    return models
