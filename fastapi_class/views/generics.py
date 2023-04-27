from typing import Generic, Type, TypeVar
from uuid import UUID

from fastapi import Depends, Response
from pydantic import BaseModel
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from ..serializer import PydanticSerializer
from ..types import Repository
from .api import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    PartialUpdateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from .functools import catch_defined
from .mixins import ErrorHandlerMixin

P = TypeVar("P", bound=Type[BaseModel])


class PK(BaseModel):
    id: UUID


class GenericViewMixin(ErrorHandlerMixin, Generic[P]):
    repository: Repository
    params: P = BaseModel

    @classmethod
    def get_params(cls, action: str) -> P:
        return cls.params


class GenericListView(ListAPIView, GenericViewMixin):
    @classmethod
    def get_list_endpoint(cls):
        param_type = cls.get_params("list")

        async def list_endpoint(
            self: GenericListView = Depends(cls),
            params: param_type = Depends(param_type),
        ):
            objects = await self.list(**params.dict(exclude_none=True))
            return await self.serialize_response(
                "list", objects, status_code=HTTP_200_OK
            )

        cls._patch_metadata(list_endpoint, cls.list)
        return list_endpoint

    @catch_defined
    async def list(self, *args, **kwargs):
        return await self.repository.list(*args, **kwargs)


class GenericCreateView(CreateAPIView, GenericViewMixin):
    create_serializer: Type[PydanticSerializer]

    @classmethod
    def get_create_endpoint(cls):
        create_serializer_type = cls.create_serializer
        param_type = cls.get_params("create")

        async def create_endpoint(
            create_serializer: create_serializer_type,
            self: GenericCreateView = Depends(cls),
            params: param_type = Depends(param_type),
        ):
            obj = await self.create(
                create_serializer=create_serializer, **params.dict(exclude_none=True)
            )
            if self.return_on_create:
                return await self.serialize_response(
                    "create", obj, status_code=HTTP_201_CREATED
                )
            return Response(status_code=HTTP_201_CREATED)

        cls._patch_metadata(create_endpoint, cls.create)
        return create_endpoint

    @catch_defined
    async def create(self, *args, **kwargs):
        return await self.repository.create(*args, **kwargs)


class GenericRetrieveView(RetrieveAPIView, GenericViewMixin):
    create_serializer: Type[PydanticSerializer]
    pk: Type[BaseModel] = PK

    @classmethod
    def get_retrieve_endpoint(cls):
        param_type = cls.get_params("retrieve")
        pk_type = cls.pk

        async def retrieve_endpoint(
            self: GenericRetrieveView = Depends(cls),
            pk: pk_type = Depends(pk_type),
            params: param_type = Depends(param_type),
        ):
            kwargs = {**pk.dict(exclude_none=True), **params.dict(exclude_none=True)}

            obj = await self.retrieve(**kwargs)
            if obj is None:
                self.raise_not_found_error()
            return await self.serialize_response("retrieve", obj)

        cls._patch_metadata(retrieve_endpoint, cls.retrieve)
        return retrieve_endpoint

    @catch_defined
    async def retrieve(self, *args, **kwargs):
        return await self.repository.retrieve(*args, **kwargs)


class GenericUpdateView(UpdateAPIView, GenericViewMixin):
    update_serializer: Type[PydanticSerializer]
    pk: Type[BaseModel] = PK

    @classmethod
    def get_update_endpoint(cls):
        update_serializer_type = cls.update_serializer
        param_type = cls.get_params("update")
        pk_type = cls.pk

        async def update_endpoint(
            update_serializer: update_serializer_type,
            self: GenericUpdateView = Depends(cls),
            pk: pk_type = Depends(pk_type),
            params: param_type = Depends(param_type),
        ):
            kwargs = {**pk.dict(exclude_none=True), **params.dict(exclude_none=True)}

            obj = await self.update(update_serializer=update_serializer, **kwargs)
            if self.return_on_update:
                return await self.serialize_response("update", obj)
            return Response(status_code=HTTP_200_OK)

        cls._patch_metadata(update_endpoint, cls.update)
        return update_endpoint

    @catch_defined
    async def update(self, *args, **kwargs):
        return await self.repository.update(*args, **kwargs)


class GenericPartialUpdateView(PartialUpdateAPIView, GenericViewMixin):
    partial_update_serializer: Type[PydanticSerializer]
    pk: Type[BaseModel] = PK

    @classmethod
    def get_partial_update_endpoint(cls):
        partial_update_serializer_type = cls.partial_update_serializer
        param_type = cls.get_params("partial_update")
        pk_type = cls.pk

        async def partial_update_endpoint(
            partial_update_serializer: partial_update_serializer_type,
            self: GenericPartialUpdateView = Depends(cls),
            pk: pk_type = Depends(pk_type),
            params: param_type = Depends(param_type),
        ):
            kwargs = {**pk.dict(exclude_none=True), **params.dict(exclude_none=True)}
            obj = await self.partial_update(
                partial_update_serializer=partial_update_serializer, **kwargs
            )
            if self.return_on_update:
                return await self.serialize_response("partial_update", obj)
            return Response(status_code=HTTP_200_OK)

        cls._patch_metadata(partial_update_endpoint, cls.partial_update)
        return partial_update_endpoint

    @catch_defined
    async def partial_update(self, *args, **kwargs):
        return await self.repository.partial_update(*args, **kwargs)


class GenericDestroyView(DestroyAPIView, GenericViewMixin):
    pk: Type[BaseModel] = PK

    @classmethod
    def get_destroy_endpoint(cls):
        param_type = cls.get_params("destroy")
        pk_type = cls.pk

        async def destroy_endpoint(
            self: GenericDestroyView = Depends(cls),
            pk: pk_type = Depends(pk_type),
            params: param_type = Depends(param_type),
        ):
            kwargs = {**pk.dict(exclude_none=True), **params.dict(exclude_none=True)}
            await self.destroy(**kwargs)
            return Response(status_code=HTTP_204_NO_CONTENT)

        cls._patch_metadata(destroy_endpoint, cls.destroy)
        return destroy_endpoint

    @catch_defined
    async def destroy(self, *args, **kwargs) -> None:
        await self.repository.delete(*args, **kwargs)
