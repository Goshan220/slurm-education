import pytest

from swagger_client import Configuration, ApiClient, PetApi, Category, Tag

HOST = "http://localhost/api/v3"


@pytest.fixture(scope="session")
def configuration():
    config = Configuration()
    config.host = HOST
    return config


@pytest.fixture(scope="session")
def api_client(configuration):
    api_client = ApiClient(configuration)
    api_client.set_default_header("Content-Type", "application/x-www-form-urlencoded")
    return api_client


@pytest.fixture(scope="module")
def pet_api(api_client):
    return PetApi(api_client)


@pytest.fixture(scope="module")
def category():
    category = Category(id=1, name="Cats")
    yield category
    del category


@pytest.fixture(scope="module")
def tags():
    tag = Tag(id=1, name="LongHaired")
    yield [tag]
    del tag
