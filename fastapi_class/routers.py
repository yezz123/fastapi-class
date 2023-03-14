from collections.abc import Callable, Iterable
from dataclasses import dataclass
from enum import Enum
from functools import wraps

from fastapi.responses import Response
from pydantic import BaseModel


class Method(str, Enum):
    GET = "get"
    POST = "post"
    PATCH = "patch"
    DELETE = "delete"
    PUT = "put"


@dataclass(frozen=True, init=True, repr=True)
class Metadata:
    methods: Iterable[Method]
    name: str | None = None
    path: str | None = None
    response_model: type[BaseModel] | None = None
    response_class: type[Response] | None = None


def endpoint(
    methods: Iterable[str | Method] | None = None,
    *,
    name: str | None = None,
    path: str | None = None,
    response_model: type[BaseModel] | None = None,
    response_class: type[Response] | None = None,
):
    """
    Endpoint decorator.

    :param methods: methods
    :param name: name
    :param path: path
    :param response_model: response model
    :param response_class: response class

    :raise AssertionError: if response model or response class is not a subclass of BaseModel or Response respectively
    :raise AssertionError: if methods is not an iterable of strings or Method enums

    :example:
    >>> from fastapi import FastAPI
    >>> from fastapi_class import endpoint
    >>> app = FastAPI()
    >>> @endpoint()
    ... def get():
    ...     return {"message": "Hello, world!"}
    >>> app.include_router(get)

    Results:

    `GET /get`
    """
    assert all(
        issubclass(_type, expected_type)
        for _type, expected_type in (
            (response_model, BaseModel),
            (response_class, Response),
        )
        if _type is not None
    ), "Response model and response class must be subclasses of BaseModel and Response respectively."
    assert (
        isinstance(methods, Iterable)
        and not isinstance(methods, str)
        or methods is None
    ), "Methods must be an iterable of strings or Method enums."

    def _decorator(function: Callable):
        @wraps(function)
        async def _wrapper(*args, **kwargs):
            return await function(*args, **kwargs)

        parsed_method = set()
        _methods = methods or ((name,) if name else (function.__name__,))
        for method in _methods:
            if isinstance(method, Method):
                parsed_method.add(method)
                continue
            try:
                parsed_method.add(Method[method.upper()])
            except KeyError as exc:
                raise ValueError(f"HTTP Method {method} is not allowed") from exc
        _wrapper.__endpoint_metadata = Metadata(
            methods=parsed_method,
            name=name,
            path=path,
            response_class=response_class,
            response_model=response_model,
        )
        return _wrapper

    return _decorator
