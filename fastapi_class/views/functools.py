import functools
from typing import Any, Callable, Tuple, Type, Union

from fastapi_class.views.mixins import ErrorHandlerMixin

VIEWSET_ROUTE_FLAG = "_is_viewset_route"


def override(**kwargs):
    def wrapper(func):
        func.kwargs = kwargs
        return func

    return wrapper


def route(**kwargs: Any) -> Callable:
    def wrapper(func: Callable):
        setattr(func, VIEWSET_ROUTE_FLAG, True)
        return override(**kwargs)(func)

    return wrapper


def catch(exc_type: Union[Type[Exception], Tuple[Type[Exception]]], **kw: Any):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(self, *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)
            except exc_type as e:
                self.handle_error(exc_type, e, **kw)

        return wrapped

    return wrapper


def catch_defined(func):
    @functools.wraps(func)
    async def wrapped(self: ErrorHandlerMixin, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except self.catches as e:
            self.handle_error(type(e), e)

    return wrapped


get = functools.partial(route, methods=["GET"])
post = functools.partial(route, methods=["POST"])
put = functools.partial(route, methods=["PUT"])
patch = functools.partial(route, methods=["PATCH"])
delete = functools.partial(route, methods=["DELETE"])
