import pytest
from fastapi import APIRouter, FastAPI, status

from fastapi_class import Method, View
from tests.factory import Factory


def decorate_view(
    app: FastAPI,
    router: APIRouter | None,
    class_base_view: object,
    default_status_code: int = status.HTTP_200_OK,
):
    View(router or app, default_status_code=default_status_code)(class_base_view)
    if router:
        app.include_router(router)


@pytest.fixture(name="application")
def fixture_application():
    yield FastAPI()


@pytest.fixture(name="router_factory")
def fixture_router_factory():
    def _factory(prefix: str = ""):
        router = APIRouter(prefix=prefix)
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

            data[_endpoint.get("alternative_name") or dummy.__name__] = _endpoint[
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
