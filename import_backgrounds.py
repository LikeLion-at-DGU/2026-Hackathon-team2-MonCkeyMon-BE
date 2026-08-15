import os
import django
import unicodedata

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.core.files import File
from products.models import Background

TAGS = {
    "일본": "후지산,신사",
    "한국": "",
    "두바이": "",
    "프랑스": "",
    "미국": "",
    "영국": "",
    "중국": "",
    "대만": "",
    "독일": "",
    "싱가포르": "",
    "캐나다": "",
    "하와이": "",
    "홍콩": "",
}

FOLDERS = [
    ("backgrounds", "나라 별"),
    ("curation", "큐레이션룸"),
]

created = 0
skipped = 0

for folder, bg_type in FOLDERS:
    if not os.path.isdir(folder):
        print(f"폴더 없음, 건너뜀: {folder}")
        continue

    for filename in sorted(os.listdir(folder)):
        if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        name = unicodedata.normalize("NFC", os.path.splitext(filename)[0]).strip()

        if Background.objects.filter(name=name).exists():
            print(f"이미 있음: {name}")
            skipped += 1
            continue

        bg = Background(name=name, type=bg_type, tags=TAGS.get(name, ""))

        with open(os.path.join(folder, filename), "rb") as img:
            bg.image.save(filename, File(img), save=False)

        bg.save()
        created += 1
        print(f"등록: {name} [{bg_type}]")

print(f"\n완료 - 등록 {created}개 / 건너뜀 {skipped}개")