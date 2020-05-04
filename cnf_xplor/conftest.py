import pytest
from django.test import RequestFactory

from cnf_xplor.users.models import User
from cnf_xplor.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()
