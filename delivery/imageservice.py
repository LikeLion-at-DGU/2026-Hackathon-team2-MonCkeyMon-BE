import os
import base64
import logging

from openai import OpenAI


logger = logging.getLogger(__name__)


def _to_openai_file(field_file):
    field_file.open("rb")

    try:
        raw = field_file.read()
    finally:
        field_file.close()

    if not raw:
        raise ValueError(
            f"'{field_file.name}' 파일에서 읽은 데이터가 비어 있습니다."
        )

    filename = os.path.basename(field_file.name)

    return (
        filename,
        raw,
        "image/png",
    )


def generate_composite_image(session):
    api_key = os.environ["OPENAI_API_KEY"]

    client = OpenAI(
        api_key=api_key
    )

    # Django ImageFieldFile → OpenAI용 파일
    person_file = _to_openai_file(
        session.person_image
    )

    bag_file = _to_openai_file(
        session.product.overlay_image
    )

    background_file = _to_openai_file(
        session.background.image
    )

    result = client.images.edit(
        model="gpt-image-2",

        image=[
            person_file,
            bag_file,
            background_file,
        ],
        quality="low",

        prompt=(
            "Create one realistic composite photograph using "
            "the three provided reference images.\n\n"

            "REFERENCE 1 — PERSON:\n"
            "Use this image as the main person. "
            "Preserve the person's identity, face, body proportions, "
            "clothing, and overall appearance.\n\n"

            "REFERENCE 2 — BAG:\n"
            "Use this image as the exact product reference. "
            "Preserve the bag's design, shape, color, logo, "
            "pattern, and proportions.\n\n"

            "REFERENCE 3 — BACKGROUND:\n"
            "Use this image as the environment/background.\n\n"

            "COMPOSITION:\n"
            "Place the person naturally into the background. "
            "Place the bag naturally in the person's hand/body position "
            "as if the person is actually holding the bag. "
            "Match the bag's scale, perspective, lighting, shadows, "
            "occlusion, and position to the person.\n\n"

            "The final result should look like a single real photograph, "
            "not a collage or three-image combination."
        ),
    )

    return base64.b64decode(
        result.data[0].b64_json
    )