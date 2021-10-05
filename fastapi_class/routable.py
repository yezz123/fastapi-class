import dataclasses
import inspect
from functools import partial
from typing import Any, Callable, Dict, List, Tuple, Type, TypeVar, cast

from fastapi.routing import APIRouter

from fastapi_class.args import EndpointDefinition

AnyCallable = TypeVar("AnyCallable", bound=Callable[..., Any])

"""
    This module contains the `Routable` class, which is used to define a class

    Returns:
        [type] -- [description]
"""


class RoutableMeta(type):
    """This is a meta-class that converts all the methods that were marked by a route/path decorator into values on a
    class member called _endpoints that the Routable constructor then uses to add the endpoints to its router."""

    def __new__(
        cls: Type[type], name: str, bases: Tuple[Type[Any]], attrs: Dict[str, Any]
    ) -> "RoutableMeta":
        endpoints: List[EndpointDefinition] = []
        # Loop through all the methods in the class
        for v in attrs.values():
            if inspect.isfunction(v) and hasattr(v, "_endpoint"):
                # If the method is marked by a route/path decorator, add it to the list of endpoints
                endpoints.append(v._endpoint)
        attrs["_endpoints"] = endpoints
        # Remove the _endpoint attribute from the class
        return cast(RoutableMeta, type.__new__(cls, name, bases, attrs))


class Routable(metaclass=RoutableMeta):
    """
    - The Routable class is a base class for all the classes that are to be used as the base for the API.
    - The Routable class is a metaclass that converts all the methods that were marked by a route/path decorator into
        values on a class member called _endpoints that the Routable constructor then uses to add the endpoints to its
        router.
    """

    _endpoints: List[EndpointDefinition] = []

    def __init__(self) -> None:
        # Create a router for the class
        self.router = APIRouter()
        # Loop through all the endpoints in the class
        for endpoint in self._endpoints:
            # The endpoint is a tuple of the endpoint name and the endpoint function
            self.router.add_api_route(
                endpoint=partial(endpoint.endpoint, self),
                **dataclasses.asdict(endpoint.args),
            )
