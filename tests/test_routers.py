from collections.abc import Callable, Iterable
from types import FunctionType

import pytest

from fastapi_class import Method, endpoint


async def dummy_function():
    pass


def assert_methods_in_metadata(_endpoint: Callable, methods: Iterable[Method]):
    assert _endpoint.__endpoint_metadata
    assert len(_endpoint.__endpoint_metadata.methods) == len(methods)
    assert all(method in _endpoint.__endpoint_metadata.methods for method in methods)


@pytest.mark.parametrize("method", Method)
def test_endpoint__correct(method: Method):
    _endpoint = endpoint((method.value,), name="test", path="/test")(dummy_function)
    assert_methods_in_metadata(_endpoint, [method])
    assert _endpoint.__endpoint_metadata.name == "test"
    assert _endpoint.__endpoint_metadata.path == "/test"


def test_endpoint__supplied_methods_can_str_or_enum():
    _endpoint = endpoint(["get", Method.POST, "PATCH", "Delete", "pUt"])(dummy_function)
    assert_methods_in_metadata(_endpoint, Method)


def test_endpoint__not_supported_method():
    with pytest.raises(ValueError):
        endpoint(("Test",))(dummy_function)


def test_endpoint__bad_response_model():
    with pytest.raises(AssertionError):
        endpoint(response_model=object)(dummy_function)


def test_endpoint__bad_response_class():
    with pytest.raises(AssertionError):
        endpoint(response_class=object)(dummy_function)


@pytest.mark.parametrize("method", Method)
def test_endpoint__method_inferred_from_name(method: Method):
    def foo():
        pass

    _endpoint = endpoint(name=method.value)(foo)
    assert_methods_in_metadata(_endpoint, [method])


@pytest.mark.parametrize("method", Method)
def test_endpoint__method_inferred_from_function_name(method: Method):
    func = FunctionType(
        compile(f"def {method.value}(): pass", f"{__name__}-t.py", "exec"),
        {},
        name=method.value,
    )
    _endpoint = endpoint(path="/test")(func)
    assert_methods_in_metadata(_endpoint, [method])
