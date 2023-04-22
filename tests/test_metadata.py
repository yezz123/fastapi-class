from typing import Any

import pytest
from fastapi.responses import Response
from pydantic import BaseModel

from fastapi_class import Metadata
from tests.factory import Factory


@pytest.fixture(name="metadata_factory")
def fixture_metadata_factory():
    def _factory(data: dict[str, Any] | None = None):
        data = data or {}
        return Metadata(
            data.get("methods", ["GET"]),
            name=data.get("name", "test"),
            path=data.get("path", "test"),
            status_code=data.get("status_code", 200),
            response_model=data.get("response_model", BaseModel),
            response_class=data.get("response_class", Response),
        )

    return _factory


@pytest.fixture(name="metadata")
def fixture_metadata(metadata_factory: Factory[Metadata]):
    return metadata_factory()


def test_metadata_dynamic_optional_fields__get_when_field_exist(metadata: Metadata):
    assert metadata.methods == ["GET"]
    assert metadata.name == "test"
    assert metadata.status_code == 200
    assert metadata.response_model == BaseModel
    assert metadata.response_class == Response


def test_metadata_dynamic_optional_fields__raise_when_field_doesnt_exist(
    metadata: Metadata,
):
    with pytest.raises(AttributeError):
        metadata.non_existing
    with pytest.raises(AttributeError):
        metadata.or_default


def test_metadata_dynamic_optional_fields_default__when_field_exists(
    metadata_factory: Factory[Metadata],
):
    metadata = metadata_factory({"name": "", "methods": [], "status_code": None})

    assert metadata.name_or_default("test") == "test"
    assert metadata.methods_or_default(["test"]) == ["test"]
    assert metadata.status_code_or_default(123) == 123


def test_metadata_dynamic_optional_fields_default__when_field_doesnt_exist(
    metadata: Metadata,
):
    with pytest.raises(AttributeError):
        metadata.non_existing_or_default("test")
