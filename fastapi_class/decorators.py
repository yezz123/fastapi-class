from typing import Any, Callable, List, TypeVar

from fastapi_class.args import EndpointDefinition, RouteArgs

AnyCallable = TypeVar("AnyCallable", bound=Callable[..., Any])
"""
    Decorators for the request body arguments.
"""


def route(
    path: str, methods: List[str], **kwargs: Any
) -> Callable[[AnyCallable], AnyCallable]:
    """
    Decorator to define a route.

    :param path: The path of the route.
    :param methods: The methods of the route.
    :param kwargs: The arguments of the route.
    :return: The decorated function.
    """

    def marker(method: AnyCallable) -> AnyCallable:
        setattr(
            method,
            "_endpoint",
            EndpointDefinition(
                endpoint=method, args=RouteArgs(path=path, methods=methods, **kwargs)
            ),
        )
        return method

    return marker


def get(path: str, **kwargs: Any) -> Callable[[AnyCallable], AnyCallable]:
    # TODO: implement
    return route(path, methods=["GET"], **kwargs)


def post(path: str, **kwargs: Any) -> Callable[[AnyCallable], AnyCallable]:
    # TODO: implement
    return route(path, methods=["POST"], **kwargs)


def put(path: str, **kwargs: Any) -> Callable[[AnyCallable], AnyCallable]:
    # TODO: implement
    return route(path, methods=["PUT"], **kwargs)


def delete(path: str, **kwargs: Any) -> Callable[[AnyCallable], AnyCallable]:
    # TODO: implement
    return route(path, methods=["DELETE"], **kwargs)


def patch(path: str, **kwargs: Any) -> Callable[[AnyCallable], AnyCallable]:
    # TODO: implement
    return route(path, methods=["PATCH"], **kwargs)


def options(path: str, **kwargs: Any) -> Callable[[AnyCallable], AnyCallable]:
    # TODO: implement
    return route(path, methods=["OPTIONS"], **kwargs)


def head(path: str, **kwargs: Any) -> Callable[[AnyCallable], AnyCallable]:
    # TODO: implement
    return route(path, methods=["HEAD"], **kwargs)
