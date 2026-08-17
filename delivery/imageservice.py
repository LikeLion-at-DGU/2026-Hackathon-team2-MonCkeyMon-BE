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

    client = OpenAI(api_key=api_key)

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

    # 상품 카테고리별 자연스러운 가방 위치
    category_position = {
        "토트백&쇼퍼백": "carry it naturally by the hand or arm",
        "숄더백&크로스백": "wear it on the shoulder or across the body",
        "백팩": "wear it on the back with the shoulder straps",
        "탑 핸들백": "carry it by the top handle in the hand",
        "트래블": "carry it naturally as travel luggage",
        "벨트백": "wear it around the waist or across the chest",
        "미니백": "carry or wear it naturally according to its shape",
        "클러치&파우치": "hold it naturally in the hand",
    }

    position = category_position.get(
        session.product.category,
        "place it in a natural position for this type of bag"
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
            "Create one realistic photograph using the three images.\n"
            "Preserve the person's appearance and clothing.\n"
            "Preserve the exact bag design, color, shape, and proportions.\n"
            "Use the third image as the background.\n"
            f"Bag category: {session.product.category}.\n"
            f"Bag placement: {position}.\n"
            "Match the bag's scale, perspective, lighting, shadows, "
            "and occlusion naturally.\n"
            "Make the final image look like one real photograph."
        ),
    )

    return base64.b64decode(
        result.data[0].b64_json
    )