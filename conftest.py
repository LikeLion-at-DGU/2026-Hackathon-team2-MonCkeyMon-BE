import pytest
from rest_framework.test import APIClient

from products.models import Background, Product


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def product(db):
    return Product.objects.create(
        name="테스트 백팩",
        category="백팩",
    )


@pytest.fixture
def background(db):
    return Background.objects.create(
        name="테스트 배경",
        type="나라 별",
    )
