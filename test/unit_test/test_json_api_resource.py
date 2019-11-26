import pytest
from unittest.mock import patch
from src import JsonApiResource, attribute, resource_id, relationship


class BaseResource(JsonApiResource):
    @staticmethod
    def base_url() -> str:
        return "http://some.url"


def test_base_url_raises_not_implemented():
    with pytest.raises(NotImplementedError, match=r"Implement this .*"):
        JsonApiResource.base_url()


@patch("src.json_api_resource.JsonApiRequest")
def test_find(json_api_request_mock):
    BaseResource.find(1)

    json_api_request_mock.return_value.find.assert_called_once_with(resource_id=1)
    json_api_request_mock.assert_called_once_with(BaseResource)


@patch("src.json_api_resource.JsonApiRequest")
def test_all(json_api_request_mock):
    BaseResource.all()

    json_api_request_mock.return_value.all.assert_called_once()
    json_api_request_mock.assert_called_once_with(BaseResource)


@patch("src.json_api_resource.JsonApiRequest")
def test_with_params(json_api_request_mock):
    BaseResource.with_params(a="b", c="d")

    json_api_request_mock.return_value.with_params.assert_called_once_with(a="b", c="d")
    json_api_request_mock.assert_called_once_with(BaseResource)


@patch("src.json_api_resource.JsonApiRequest")
def test_where(json_api_request_mock):
    BaseResource.where(a="b", c="d")

    json_api_request_mock.return_value.where.assert_called_once_with(a="b", c="d")
    json_api_request_mock.assert_called_once_with(BaseResource)


def test_attributes():
    class Resource(BaseResource):
        attribute1: int = attribute()
        attribute2: str = attribute()

    assert Resource.attributes() == ["attribute1", "attribute2"]


def test_relationships():
    class Relationship(BaseResource):
        id: str = resource_id()

    class Resource(BaseResource):
        id: str = resource_id()
        relationship1: Relationship = relationship()

    assert Resource.relationships() == ["relationship1"]


def test_resource_name():
    class SomeResource(BaseResource):
        pass

    assert SomeResource.resource_name() == "some-resources"


def test_base_url():
    class Resource(BaseResource):
        pass

    assert Resource.base_url() == "http://some.url"


def test_build_new_resource():
    class Resource(BaseResource):
        id: str = resource_id()
        attribute1: str = attribute()

    result = Resource(id="42", attribute1="value")

    assert result.id == "42"
    assert result.attribute1 == "value"
