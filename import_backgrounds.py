import os
import django
import unicodedata

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.core.files import File
from products.models import Background

BG_DIR = "backgrounds"
BG_TYPE = "나라 별"

created = 0
skipped = 0

for filename in sorted(os.listdir(BG_DIR)):
    if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    path = os.path.join(BG_DIR, filename)
    name = unicodedata.normalize("NFC", os.path.splitext(filename)[0]).strip()

    if Background.objects.filter(name=name).exists():
        print(f"이미 있음: {name}")
        skipped += 1
        continue

    bg = Background(name=name, type=BG_TYPE)

    with open(path, "rb") as img:
        bg.image.save(filename, File(img), save=False)

    bg.save()
    created += 1
    print(f"등록: {name}")

print(f"\n완료 - 등록 {created}개 / 건너뜀 {skipped}개")