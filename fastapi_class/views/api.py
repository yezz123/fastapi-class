import inspect
from abc import ABC, abstractmethod
from typing import (
    Any,
    AsyncIterable,
    Callable,
    Dict,
    Generator,
    Generic,
    Iterable,
    Iterator,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    get_type_hints,
)

from fastapi import Depends, Request, Response
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from ..errors import errors
from ..response import JsonResponse
from ..serializer import PydanticSerializer
from .functools import VIEWSET_ROUTE_FLAG
from .mixins import DetailViewMixin, ErrorHandlerMixin

S = TypeVar("S", bound=Type[PydanticSerializer])
P = Iterator[Dict[str, Any]]

L = TypeVar("L", bound=Union[AsyncIterable[Any], Iterable[Any]])


class View(ABC):
    api_component_name: str
    default_response_class: Type[Response] = JsonResponse

    def __init__(self, request: Request, response: Response):
        self.request = request
        self.response = response

    @classmethod
    def get_name(cls):
        return getattr(cls, "api_component_name", cls.__name__)

    @classmethod
    def get_slug_name(cls):
        return f"{cls.get_name().lower().replace(' ', '_')}"

    @classmethod
    def get_api_actions(cls, prefix: str = ""):
        yield from cls.get_custom_api_actions(prefix)

    @classmethod
    def get_custom_api_actions(cls, prefix: str = ""):
        for _, route_endpoint in inspect.getmembers(
            cls, lambda member: callable(member) and hasattr(member, VIEWSET_ROUTE_FLAG)
        ):

            def decorator(f):
                async def dec_endpoint(self, *args, **kwargs):
                    obj = await f(self, *args, **kwargs)
                    return self.get_response(content=obj)

                return dec_endpoint

            endpoint = decorator(route_endpoint)

            cls._patch_endpoint_signature(endpoint, route_endpoint)
            yield cls.get_api_action(
                endpoint, prefix=prefix, name=f"{endpoint.__name__} {cls.get_name()}"
            )

    @classmethod
    def get_api_action(
        cls, endpoint: Callable, prefix: str = "", path: str = "", **kwargs
    ) -> Dict[str, Any]:
        kw = getattr(endpoint, "kwargs", {})
        kwargs.update(kw)
        path = kwargs.get("path", path)
        kwargs["endpoint"] = endpoint
        kwargs["path"] = prefix + path
        kwargs.setdefault("name", endpoint.__name__)
        endpoint_name = kwargs["name"]
        kwargs.setdefault("methods", ["GET"])
        kwargs.setdefault("response_model", get_type_hints(endpoint).get("return"))
        kwargs.setdefault("operation_id", f"{cls.get_slug_name()}_{endpoint_name}")

        return kwargs

    @classmethod
    def _patch_metadata(cls, endpoint, method: Callable) -> None:
        endpoint.__doc__ = method.__doc__
        endpoint.__name__ = method.__name__
        endpoint.kwargs = getattr(method, "kwargs", {})

    @classmethod
    def _patch_endpoint_signature(cls, endpoint, method: Callable) -> None:
        old_signature = inspect.signature(method)
        old_parameters: list[inspect.Parameter] = list(
            old_signature.parameters.values()
        )
        old_first_parameter = old_parameters[0]
        new_first_parameter = old_first_parameter.replace(default=Depends(cls))
        new_parameters = [new_first_parameter] + [
            parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY)
            for parameter in old_parameters[1:]
        ]
        new_signature = old_signature.replace(parameters=new_parameters)
        endpoint.__signature__ = new_signature
        cls._patch_metadata(endpoint, method)

    def get_response(self, content: Any) -> Response:
        if isinstance(content, Response):
            return content
        return self.default_response_class(
            content=content,
            status_code=self.response.status_code or HTTP_200_OK,
            headers=dict(self.response.headers),
        )


class APIView(View, ErrorHandlerMixin, Generic[S]):
    serializer: S

    @classmethod
    def get_serializer(cls, action: str) -> S:
        return cls.serializer

    async def serialize_response(
        self, action: str, content: Any, status_code: int = HTTP_200_OK
    ):
        if content:
            serializer = self.get_serializer(action)
            content = await serializer.parse(content)
        if self.response.status_code is None:
            self.response.status_code = status_code
        return self.get_response(content)


class ListAPIView(APIView, Generic[L]):
    serializer_to_list: bool = True

    @abstractmethod
    async def list(self, *args, **kwargs) -> L:
        raise NotImplementedError

    @classmethod
    def get_list_endpoint(cls):
        async def endpoint(self: ListAPIView, *args, **kwargs):
            objects = await self.list(*args, **kwargs)
            return await self.serialize_response("list", objects)

        cls._patch_endpoint_signature(endpoint, cls.list)
        return endpoint

    @classmethod
    def get_api_actions(cls, prefix: str = ""):
        response_model = (
            List[cls.get_serializer("list")]
            if cls.serializer_to_list
            else cls.get_serializer("list")
        )
        yield cls.get_api_action(
            prefix=prefix,
            endpoint=cls.get_list_endpoint(),
            methods=["GET"],
            response_model=response_model,
            name=f"List {cls.get_name()}",
            operation_id=f"list_{cls.get_slug_name()}",
        )
        yield from super().get_api_actions(prefix)


class RetrieveAPIView(APIView, DetailViewMixin):
    @classmethod
    def get_retrieve_endpoint(cls):
        async def endpoint(self: RetrieveAPIView, *args, **kwargs):
            obj = await self.retrieve(*args, **kwargs)
            if obj is None and self.raise_on_none:
                self.raise_not_found_error()
            return await self.serialize_response("retrieve", obj)

        cls._patch_endpoint_signature(endpoint, cls.retrieve)
        return endpoint

    @classmethod
    def get_api_actions(cls, prefix: str = ""):
        yield cls.get_api_action(
            prefix=prefix,
            endpoint=cls.get_retrieve_endpoint(),
            path=cls.get_detail_route(action="retrieve"),
            methods=["GET"],
            responses=errors(404),
            response_model=cls.get_serializer(action="retrieve"),
            name=f"Get {cls.get_name()}",
            operation_id=f"get_{cls.get_slug_name()}",
        )
        yield from super().get_api_actions(prefix)

    @abstractmethod
    async def retrieve(self, *args, **kwargs) -> Optional[Any]:
        raise NotImplementedError


class CreateAPIView(APIView):
    return_on_create: bool = True

    @classmethod
    def get_create_endpoint(cls):
        async def endpoint(self: CreateAPIView, *args, **kwargs):
            obj = await self.create(*args, **kwargs)
            if self.return_on_create:
                return await self.serialize_response("create", obj, HTTP_201_CREATED)
            return Response(status_code=HTTP_201_CREATED)

        cls._patch_endpoint_signature(endpoint, cls.create)
        return endpoint

    @classmethod
    def get_api_actions(cls, prefix: str = ""):
        yield cls.get_api_action(
            prefix=prefix,
            endpoint=cls.get_create_endpoint(),
            methods=["POST"],
            status_code=201,
            responses=errors(409, 422),
            response_model=cls.get_serializer(action="create"),
            name=f"Create {cls.get_name()}",
            operation_id=f"create_{cls.get_slug_name()}",
        )
        yield from super().get_api_actions(prefix)

    @abstractmethod
    async def create(self, *args, **kwargs) -> Any:
        raise NotImplementedError


class UpdateAPIView(APIView, DetailViewMixin):
    return_on_update: bool = True

    @classmethod
    def get_update_endpoint(cls):
        async def endpoint(self: UpdateAPIView, *args, **kwargs):
            obj = await self.update(*args, **kwargs)
            if not self.return_on_update:
                return Response(status_code=HTTP_200_OK)
            if obj is None and self.raise_on_none:
                self.raise_not_found_error()
            return await self.serialize_response("update", obj)

        cls._patch_endpoint_signature(endpoint, cls.update)
        return endpoint

    @classmethod
    def get_api_actions(cls, prefix: str = ""):
        yield cls.get_api_action(
            prefix=prefix,
            path=cls.get_detail_route(action="update"),
            endpoint=cls.get_update_endpoint(),
            methods=["PUT"],
            responses=errors(HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY),
            response_model=cls.get_serializer(action="update"),
            name=f"Update {cls.get_name()}",
            operation_id=f"update_{cls.get_slug_name()}",
        )
        yield from super().get_api_actions(prefix)

    @abstractmethod
    async def update(self, *args, **kwargs):
        raise NotImplementedError


class PartialUpdateAPIView(APIView, DetailViewMixin):
    return_on_update: bool = True

    @classmethod
    def get_partial_update_endpoint(cls):
        async def endpoint(self: PartialUpdateAPIView, *args, **kwargs):
            obj = await self.partial_update(*args, **kwargs)
            if obj is None and self.raise_on_none:
                self.raise_not_found_error()
            if self.return_on_update:
                return await self.serialize_response("partial_update", obj)
            return Response(status_code=HTTP_200_OK)

        cls._patch_endpoint_signature(endpoint, cls.partial_update)
        return endpoint

    @classmethod
    def get_api_actions(cls, prefix: str = "") -> Generator:
        yield cls.get_api_action(
            prefix=prefix,
            path=cls.get_detail_route(action="update"),
            endpoint=cls.get_partial_update_endpoint(),
            methods=["PATCH"],
            responses=errors(HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY),
            response_model=cls.get_serializer(action="update"),
            name=f"Partial update {cls.get_name()}",
            operation_id=f"patch_{cls.get_slug_name()}",
        )

        yield from super().get_api_actions(prefix)

    @abstractmethod
    async def partial_update(self, *args, **kwargs):
        raise NotImplementedError


class DestroyAPIView(APIView, DetailViewMixin):
    @classmethod
    def get_destroy_endpoint(cls):
        async def endpoint(self: DestroyAPIView, *args, **kwargs):
            await self.destroy(*args, **kwargs)
            return Response(status_code=HTTP_204_NO_CONTENT)

        cls._patch_endpoint_signature(endpoint, cls.destroy)
        return endpoint

    @classmethod
    def get_api_actions(cls, prefix: str = "") -> Generator:
        yield cls.get_api_action(
            prefix=prefix,
            path=cls.get_detail_route(action="destroy"),
            endpoint=cls.get_destroy_endpoint(),
            methods=["DELETE"],
            response_class=Response,
            status_code=HTTP_204_NO_CONTENT,
            name=f"Delete {cls.get_name()}",
            operation_id=f"delete_{cls.get_slug_name()}",
        )
        yield from super().get_api_actions(prefix)

    @abstractmethod
    async def destroy(self, *args, **kwargs) -> None:
        raise NotImplementedError
