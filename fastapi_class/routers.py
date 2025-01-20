from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from enum import Enum
from functools import wraps
from typing import Any, ClassVar

from fastapi.responses import Response
from pydantic import BaseModel


class Method(str, Enum):
    """HTTP methods."""

    GET = "get"
    POST = "post"
    PATCH = "patch"
    DELETE = "delete"
    PUT = "put"


@dataclass(frozen=True, init=True, repr=True)
class Metadata:
    """Metadata class, used to store endpoint metadata."""

    methods: Iterable[str | Method]
    name: str | None = None
    path: str | None = None
    status_code: int | None = None
    response_model: type[BaseModel] | None = None
    response_class: type[Response] | None = None
    __default_method_suffix: ClassVar[str] = "_or_default"

    def __getattr__(self, __name: str, /) -> Any | Callable[[Any], Any]:
        """Dynamically return the value of the attribute."""
        if __name.endswith(Metadata.__default_method_suffix):
            prefix = __name.replace(Metadata.__default_method_suffix, "")
            if hasattr(self, prefix):
                return lambda _default: getattr(self, prefix, None) or _default
            return getattr(self, prefix)
        raise AttributeError(f"{self.__class__.__name__} has no attribute {__name}")


def endpoint(
    methods: Iterable[str | Method] | str | None = None,
    *,
    name: str | None = None,
    path: str | None = None,
    status_code: int | None = None,
    response_model: type[BaseModel] | None = None,
    response_class: type[Response] | None = None,
):
    """Endpoint decorator for FastAPI.

    ### Example:
        >>> from fastapi import FastAPI
        >>> from fastapi_class import endpoint
        >>> app = FastAPI()
        >>> @endpoint()
        ... async def get():
        ...     return {"message": "Hello, world!"}
        >>> app.include_router(get)
    """
    assert all(
        issubclass(_type, expected_type)
        for _type, expected_type in (
            (response_model, BaseModel),
            (response_class, Response),
        )
        if _type is not None
    ), "Response model and response class must be subclasses of BaseModel and Response respectively."
    assert isinstance(methods, (Iterable, str)) or methods is None, (
        "Methods must be an string, iterable of strings or Method enums."
    )

    def _decorator(function: Callable):
        """Decorate the function."""

        @wraps(function)
        async def _wrapper(*args, **kwargs):
            """Wrapper for the function."""
            return await function(*args, **kwargs)

        parsed_method = set()
        _methods = (methods,) if isinstance(methods, str) else methods or ((name,) if name else (function.__name__,))
        for method in _methods:
            if isinstance(method, Method):
                parsed_method.add(method)
                continue
            try:
                parsed_method.add(Method[method.upper()])
            except KeyError as exc:
                raise ValueError(f"HTTP Method {method} is not allowed") from exc
        _wrapper.__endpoint_metadata = Metadata(  # type: ignore
            methods=parsed_method,
            name=name,
            path=path,
            status_code=status_code,
            response_class=response_class,
            response_model=response_model,
        )
        return _wrapper

    return _decorator
