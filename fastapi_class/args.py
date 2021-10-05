from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Type, Union

from fastapi import Response, params
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.routing import Route

SetIntStr = Set[Union[int, str]]
DictIntStrAny = Dict[Union[int, str], Any]

"""
    args: This file contains the definition of the arguments that are passed to the functions.
"""


@dataclass
class RouteArgs:
    """
    This class contains the arguments that are passed to the functions.

    Attributes:
        path: str
        response_model: Optional[Type[Any]] = None
        status_code: Optional[int] = None
        tags: Optional[List[str]] = None
        dependencies: Optional[Sequence[params.Depends]] = None
        summary: Optional[str] = None
        description: Optional[str] = None
        response_description: str = "Successful Response"
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None
        deprecated: Optional[bool] = None
        methods: Optional[Union[Set[str], List[str]]] = None
        operation_id: Optional[str] = None
        response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None
        response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None
        response_model_by_alias: bool = True
        response_model_exclude_unset: bool = False
        response_model_exclude_defaults: bool = False
        response_model_exclude_none: bool = False
        include_in_schema: bool = True
        response_class: Union[Type[Response], DefaultPlaceholder] = Default(JSONResponse)
        name: Optional[str] = None
        route_class_override: Optional[Type[APIRoute]] = None
        callbacks: Optional[List[Route]] = None
        openapi_extra: Optional[Dict[str, Any]] = None
    """

    path: str
    response_model: Optional[Type[Any]] = None
    status_code: Optional[int] = None
    tags: Optional[List[str]] = None
    dependencies: Optional[Sequence[params.Depends]] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    response_description: str = "Successful Response"
    responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None
    deprecated: Optional[bool] = None
    methods: Optional[Union[Set[str], List[str]]] = None
    operation_id: Optional[str] = None
    response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None
    response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None
    response_model_by_alias: bool = True
    response_model_exclude_unset: bool = False
    response_model_exclude_defaults: bool = False
    response_model_exclude_none: bool = False
    include_in_schema: bool = True
    response_class: Union[Type[Response], DefaultPlaceholder] = Default(JSONResponse)
    name: Optional[str] = None
    route_class_override: Optional[Type[APIRoute]] = None
    callbacks: Optional[List[Route]] = None
    openapi_extra: Optional[Dict[str, Any]] = None

    class Config:
        """
        Config for `RouteArgs`.
        """

        arbitrary_types_allowed = True


@dataclass
class EndpointDefinition:
    """RouteArgs plus the endpoint.

    Endpoint is separate as it has to be bound to self before it can be used.
    """

    endpoint: Callable[..., Any]
    args: RouteArgs
