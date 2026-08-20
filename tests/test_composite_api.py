import io
from unittest.mock import patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image

from experiences.models import ExperienceSession


def _fake_image_file(name="person.png"):
    buffer = io.BytesIO()
    Image.new("RGB", (10, 10), color="white").save(buffer, format="PNG")
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/png")


@pytest.mark.django_db
def test_composite_without_selection_returns_400(api_client):
    session = ExperienceSession.objects.create()

    res = api_client.post(reverse("composite-image", args=[session.id]))

    assert res.status_code == 400


@pytest.mark.django_db
def test_composite_openai_failure_returns_502(api_client, product, background, caplog):
    session = ExperienceSession.objects.create(
        product=product,
        background=background,
        person_image=_fake_image_file(),
    )

    with patch(
        "delivery.views.generate_composite_image",
        side_effect=RuntimeError("openai down"),
    ):
        with caplog.at_level("ERROR", logger="delivery.views"):
            res = api_client.post(reverse("composite-image", args=[session.id]))

    assert res.status_code == 502

    view_records = [r for r in caplog.records if r.name == "delivery.views"]
    assert len(view_records) == 1
    record = view_records[0]
    assert str(session.id) in record.getMessage()
    assert record.exc_info is not None
    assert record.exc_info[0] is RuntimeError


@pytest.mark.django_db
def test_composite_success_returns_200(api_client, product, background):
    session = ExperienceSession.objects.create(
        product=product,
        background=background,
        person_image=_fake_image_file(),
    )

    buffer = io.BytesIO()
    Image.new("RGB", (10, 10), color="white").save(buffer, format="PNG")
    fake_result = buffer.getvalue()

    with patch(
        "delivery.views.generate_composite_image",
        return_value=fake_result,
    ):
        res = api_client.post(reverse("composite-image", args=[session.id]))

    assert res.status_code == 200
    assert "image_url" in res.data
