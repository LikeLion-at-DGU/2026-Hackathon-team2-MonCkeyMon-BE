from datetime import date, timedelta

import pytest
from django.urls import reverse

from experiences.models import ExperienceSession


def _select_product(api_client, product):
    session = ExperienceSession.objects.create()
    return api_client.patch(
        reverse("experiences:detail", args=[session.id]),
        {"product_id": product.id},
    )


@pytest.mark.django_db
def test_category_session_top5_default_is_cumulative(api_client, product):
    _select_product(api_client, product)
    _select_product(api_client, product)

    res = api_client.get(reverse("category-session-top5"))

    assert res.status_code == 200
    row = next(r for r in res.data if r["category"] == product.category)
    assert row["session_count"] == 2


@pytest.mark.django_db
def test_category_session_top5_today_ignores_stale_previous_day_count(api_client, product):
    product.today_choose_count = 42
    product.today_choose_date = date.today() - timedelta(days=1)
    product.choose_count = 42
    product.save()

    res = api_client.get(reverse("category-session-top5"), {"period": "today"})

    assert res.status_code == 200
    row = next((r for r in res.data if r["category"] == product.category), None)
    assert row is None or row["session_count"] == 0


@pytest.mark.django_db
def test_category_session_top5_today_reflects_todays_selections(api_client, product):
    _select_product(api_client, product)
    _select_product(api_client, product)
    _select_product(api_client, product)

    res_today = api_client.get(reverse("category-session-top5"), {"period": "today"})
    res_total = api_client.get(reverse("category-session-top5"))

    row_today = next(r for r in res_today.data if r["category"] == product.category)
    row_total = next(r for r in res_total.data if r["category"] == product.category)

    assert row_today["session_count"] == 3
    assert row_total["session_count"] == 3
