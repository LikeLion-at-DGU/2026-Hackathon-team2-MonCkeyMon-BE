import os
import csv
import django
import unicodedata

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.core.files import File
from products.models import Background

CSV_FILE = "backgrounds.csv"
SOURCE_DIRS = [d for d in ("backgrounds", "curation", "media/backgrounds")
               if os.path.isdir(d)]


def norm(s):
    """악센트·특수문자·공백 무시하고 글자만 비교"""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return "".join(c for c in s if c.isalnum()).lower()


def find_file(filename):
    target = norm(os.path.splitext(filename)[0])
    for d in SOURCE_DIRS:
        for f in os.listdir(d):
            if norm(os.path.splitext(f)[0]) == target:
                return os.path.join(d, f)
    return None


created = 0
skipped = 0

with open(CSV_FILE, encoding="utf-8-sig") as fp:
    for row in csv.DictReader(fp):
        filename = row["filename"].strip()
        name = row["name"].strip()

        if Background.objects.filter(name=name).exists():
            print(f"이미 있음: {name}")
            skipped += 1
            continue

        path = find_file(filename)
        if not path:
            print(f"파일 없음: {filename}")
            skipped += 1
            continue

        bg = Background(
            name=name,
            type=row["type"].strip(),
            tags=row["tags"].strip(),
        )

        norm_path = path.replace("\\", "/")
        if norm_path.startswith("media/"):
            # 이미 media 안에 있는 파일이면 경로만 연결 (복사 안 함)
            bg.image.name = norm_path[len("media/"):]
            bg.save()
        else:
            with open(path, "rb") as img:
                bg.image.save(filename, File(img), save=True)

        created += 1
        print(f"등록: {name} [{bg.type}]")

print(f"\n완료 - 등록 {created}개 / 건너뜀 {skipped}개")