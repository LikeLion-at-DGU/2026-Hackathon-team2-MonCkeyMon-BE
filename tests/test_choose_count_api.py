from datetime import date, timedelta

import pytest
from django.urls import reverse

from experiences.models import ExperienceSession


def _select_background(api_client, background):
    session = ExperienceSession.objects.create()
    return api_client.patch(
        reverse("experiences:detail", args=[session.id]),
        {"background_id": background.id},
    )


@pytest.mark.django_db
def test_selecting_background_increments_cumulative_and_today_count(api_client, background):
    assert background.choose_count == 0
    assert background.today_choose_count == 0

    res = _select_background(api_client, background)
    assert res.status_code == 200

    background.refresh_from_db()
    assert background.choose_count == 1
    assert background.today_choose_count == 1
    assert background.today_choose_date == date.today()


@pytest.mark.django_db
def test_choose_count_default_is_cumulative(api_client, product, background):
    _select_background(api_client, background)
    _select_background(api_client, background)

    res = api_client.get(reverse("choose-count"))

    assert res.status_code == 200
    row = next(r for r in res.data["backgrounds"] if r["id"] == background.id)
    assert row["choose_count"] == 2


@pytest.mark.django_db
def test_choose_count_today_ignores_stale_previous_day_count(api_client, background):
    background.today_choose_count = 42
    background.today_choose_date = date.today() - timedelta(days=1)
    background.choose_count = 42
    background.save()

    res = api_client.get(reverse("choose-count"), {"period": "today"})

    assert res.status_code == 200
    row = next(r for r in res.data["backgrounds"] if r["id"] == background.id)
    assert row["choose_count"] == 0


@pytest.mark.django_db
def test_choose_count_top5_today_reflects_only_todays_selections(api_client, background):
    _select_background(api_client, background)
    _select_background(api_client, background)
    _select_background(api_client, background)

    res_today = api_client.get(reverse("choose-count-top5"), {"period": "today"})
    res_total = api_client.get(reverse("choose-count-top5"))

    row_today = next(r for r in res_today.data["backgrounds"] if r["id"] == background.id)
    row_total = next(r for r in res_total.data["backgrounds"] if r["id"] == background.id)

    assert row_today["choose_count"] == 3
    assert row_total["choose_count"] == 3
