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
def test_total_visitor_count_matches_sum_of_product_selections(api_client, product):
    ExperienceSession.objects.create()
    ExperienceSession.objects.create()

    _select_product(api_client, product)
    _select_product(api_client, product)

    res = api_client.get(reverse("visitor-count"))

    assert res.status_code == 200
    assert res.data["total_visitor_count"] == 2


@pytest.mark.django_db
def test_today_visitor_count_matches_sum_of_todays_product_selections(api_client, product):
    _select_product(api_client, product)
    _select_product(api_client, product)
    _select_product(api_client, product)

    res = api_client.get(reverse("visitor-count-today"))

    assert res.status_code == 200
    assert res.data["today_visitor_count"] == 3


@pytest.mark.django_db
def test_today_visitor_count_ignores_stale_previous_day_count(api_client, product):
    product.today_choose_count = 99
    product.today_choose_date = date.today() - timedelta(days=1)
    product.choose_count = 99
    product.save()

    res = api_client.get(reverse("visitor-count-today"))

    assert res.status_code == 200
    assert res.data["today_visitor_count"] == 0
