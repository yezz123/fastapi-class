import re
from collections.abc import Callable, Iterable

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import JSONResponse

from fastapi_class.openapi import _exceptions_to_responses
from fastapi_class.routers import Metadata, Method


def _view_class_name_default_parser(cls: object, method: str):
    class_name = " ".join(re.findall(r"[A-Z][^A-Z]*", cls.__name__.replace("View", "")))
    return f"{method.capitalize()} {class_name}"


COMMON_KEYWORD = "common"
RESPONSE_MODEL_ATTRIBUTE_NAME = "RESPONSE_MODEL"
RESPONSE_CLASS_ATTRIBUTE_NAME = "RESPONSE_CLASS"
ENDPOINT_METADATA_ATTRIBUTE_NAME = "ENDPOINT_METADATA"
EXCEPTIONS_ATTRIBUTE_NAME = "EXCEPTIONS"


def View(
    router: FastAPI | APIRouter,
    *,
    path: str = "/",
    name_parser: Callable[[object, str], str] = _view_class_name_default_parser,
):
    """
    Class-based view decorator.

    :param router: router
    :param path: path
    :param name_parser: name parser

    :raise AssertionError: if router is not an instance of FastAPI or APIRouter

    :example:
    >>> from fastapi import FastAPI
    >>> from fastapi_class import View
    >>> app = FastAPI()
    >>> @View(app)
    ... class MyView:
    ...     def get(self):
    ...         return {"message": "Hello, world!"}
    >>> app.include_router(MyView.router)

    Results:

    `GET /my-view`
    """

    def _decorator(cls) -> None:
        obj = cls()
        cls_based_response_model = getattr(obj, RESPONSE_MODEL_ATTRIBUTE_NAME, {})
        cls_based_response_class = getattr(obj, RESPONSE_CLASS_ATTRIBUTE_NAME, {})
        common_exceptions = getattr(obj, EXCEPTIONS_ATTRIBUTE_NAME, {}).get(
            COMMON_KEYWORD, ()
        )
        for _callable_name in dir(obj):
            _callable = getattr(obj, _callable_name)
            if _callable_name in set(Method) or hasattr(
                _callable, ENDPOINT_METADATA_ATTRIBUTE_NAME
            ):
                metadata: Metadata | None = getattr(
                    _callable, ENDPOINT_METADATA_ATTRIBUTE_NAME, None
                )
                response_model = (
                    metadata.response_model
                    if metadata and metadata.response_model
                    else cls_based_response_model.get(_callable_name)
                )
                response_class = (
                    metadata.response_class
                    if metadata and metadata.response_class
                    else cls_based_response_class.get(_callable_name, JSONResponse)
                )
                exceptions: Iterable[HTTPException] = getattr(
                    obj, ENDPOINT_METADATA_ATTRIBUTE_NAME, {}
                ).get(_callable_name, [])
                exceptions += common_exceptions
                method = list(metadata.methods) if metadata else [_callable_name]
                name = (
                    metadata.name
                    if metadata and metadata.name
                    else name_parser(cls, _callable_name)
                )
                _path = path
                if metadata and metadata.path:
                    _path = path + metadata.path
                router.add_api_route(
                    _path,
                    _callable,
                    methods=method,
                    response_class=response_class,
                    response_model=response_model,
                    responses=_exceptions_to_responses(exceptions),
                    name=name,
                )

    return _decorator
