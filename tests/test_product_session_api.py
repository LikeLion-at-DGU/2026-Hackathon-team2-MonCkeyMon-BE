from datetime import date, timedelta

import pytest
from django.urls import reverse

from experiences.models import ExperienceSession
from products.models import Product


def _select_product(api_client, product):
    session = ExperienceSession.objects.create()
    return api_client.patch(
        reverse("experiences:detail", args=[session.id]),
        {"product_id": product.id},
    )


@pytest.mark.django_db
def test_selecting_product_increments_cumulative_and_today_count(api_client, product):
    assert product.choose_count == 0
    assert product.today_choose_count == 0

    res = _select_product(api_client, product)
    assert res.status_code == 200

    product.refresh_from_db()
    assert product.choose_count == 1
    assert product.today_choose_count == 1
    assert product.today_choose_date == date.today()


@pytest.mark.django_db
def test_product_session_default_returns_cumulative(api_client, product):
    _select_product(api_client, product)
    _select_product(api_client, product)

    res = api_client.get(reverse("product-session"))

    assert res.status_code == 200
    row = next(r for r in res.data if r["id"] == product.id)
    assert row["session_count"] == 2


@pytest.mark.django_db
def test_product_session_today_ignores_stale_previous_day_count(api_client, product):
    product.today_choose_count = 99
    product.today_choose_date = date.today() - timedelta(days=1)
    product.choose_count = 99
    product.save()

    res = api_client.get(reverse("product-session"), {"period": "today"})

    assert res.status_code == 200
    row = next(r for r in res.data if r["id"] == product.id)
    assert row["session_count"] == 0


@pytest.mark.django_db
def test_product_session_today_reflects_todays_selections_only(api_client, product):
    _select_product(api_client, product)
    _select_product(api_client, product)

    res_today = api_client.get(reverse("product-session"), {"period": "today"})
    res_total = api_client.get(reverse("product-session"))

    row_today = next(r for r in res_today.data if r["id"] == product.id)
    row_total = next(r for r in res_total.data if r["id"] == product.id)

    assert row_today["session_count"] == 2
    assert row_total["session_count"] == 2
