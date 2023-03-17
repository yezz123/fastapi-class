from typing import Any, Generic, TypeVar

import pytest
from fastapi import APIRouter, FastAPI

from fastapi_class import Method, View, endpoint

T = TypeVar("T")


class Factory(Generic[T]):
    def __call__(self, *args: Any, **kwds: Any) -> T:
        ...


def decorate_view(app: FastAPI, router: APIRouter | None, class_base_view: object):
    View(router or app)(class_base_view)
    if router:
        app.include_router(router)


@pytest.fixture(name="application")
def fixture_application():
    yield FastAPI()


@pytest.fixture(name="router_factory")
def fixture_router_factory():
    def _factory():
        router = APIRouter()
        return router

    return _factory


@pytest.fixture(name="class_base_view_factory")
def fixture_class_base_view_factory():
    def _factory(
        data: dict | None = None,
        methods=None,
        name: str = "TestClassBasedView",
        endpoints=None,
    ):
        data = data or {}
        methods = methods or []
        endpoints = endpoints or []
        for method in methods:

            def dummy(self):
                ...

            dummy.__name__ = method.value
            data[method.value] = dummy
        for _endpoint in endpoints:

            def dummy(self):
                ...

            data[dummy.__name__ or _endpoint["alternative_name"]] = _endpoint[
                "decorator"
            ](dummy)
        class_base_view = type(name, (object,), data)

        return class_base_view

    return _factory


def test_view__use_name_of_functions_as_methods(
    application: FastAPI,
    class_base_view_factory: Factory[object],
    router_factory: Factory[APIRouter],
):
    router = router_factory()
    class_base_view = class_base_view_factory(methods=Method)
    decorate_view(application, router, class_base_view)
    schema = application.openapi()
    for method in Method:
        assert "/" in schema["paths"]
        assert method.value in schema["paths"]["/"]
        assert (
            schema["paths"]["/"][method.value]["summary"]
            == f"{method.value.capitalize()} Test Class Based"
        )
        responses = schema["paths"]["/"][method.value]["responses"]
        assert "200" in responses


@pytest.mark.skip(reason="The assertion is not working")
def test_view__use_name_in_endpoint_decorator(
    application: FastAPI,
    class_base_view_factory: Factory[object],
    router_factory: Factory[APIRouter],
):
    router = router_factory()
    class_base_view = class_base_view_factory(
        endpoints=[
            {
                "decorator": endpoint(
                    methods=["POST"], name="Edit Test Class Based", path="edit"
                )
            }
        ]
    )
    decorate_view(application, router, class_base_view)
    schema = application.openapi()
    assert "/edit" in schema["paths"]
    assert "post" in schema["paths"]["/edit"]
    assert schema["paths"]["/edit"]["post"]["summary"] == "Edit Test Class Based"
