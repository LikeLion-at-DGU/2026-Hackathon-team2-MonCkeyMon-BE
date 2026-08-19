import pytest
from django.urls import reverse

from experiences.models import ExperienceSession


@pytest.mark.django_db
def test_select_background_increases_choose_count(api_client, background):
    session = ExperienceSession.objects.create()
    before = background.choose_count

    res = api_client.patch(
        reverse("experiences:detail", args=[session.id]),
        {"background_id": background.id},
    )

    assert res.status_code == 200

    background.refresh_from_db()
    assert background.choose_count == before + 1
