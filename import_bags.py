import os
import csv
import django
import unicodedata

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.core.files import File
from products.models import Product

CSV_FILE = "bags.csv"
MEDIA_DIR = "media/products/overlays"
BAGS_DIR = "bags" if os.path.isdir("bags") else MEDIA_DIR


def norm(s):
    """악센트·특수문자·공백 무시하고 글자만 비교"""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return "".join(c for c in s if c.isalnum()).lower()


def find_file(filename):
    path = os.path.join(BAGS_DIR, filename)
    if os.path.exists(path):
        return path

    target = norm(os.path.splitext(filename)[0])
    for f in os.listdir(BAGS_DIR):
        if norm(os.path.splitext(f)[0]) == target:
            return os.path.join(BAGS_DIR, f)
    return None


created = 0
skipped = 0

with open(CSV_FILE, encoding="utf-8-sig") as fp:
    for row in csv.DictReader(fp):
        filename = row["filename"].strip()
        name = row["name"].strip()
        color = row["color"].strip()
        size = row["size"].strip()

        if Product.objects.filter(name=name, color=color, size=size).exists():
            print(f"이미 있음: {name} ({color}/{size})")
            skipped += 1
            continue

        path = find_file(filename)
        if not path:
            print(f"파일 없음: {filename}")
            skipped += 1
            continue

        product = Product(
            name=name,
            color=color,
            size=size,
            gender=row["gender"].strip() or "FEMALE",
            category=row["category"].strip(),
            is_new=row["is_new"].strip().upper() == "TRUE",
            purchase_url=row["purchase_url"].strip() or None,
        )

        norm_path = path.replace("\\", "/")
        if norm_path.startswith("media/"):
            # 이미 media 안에 있는 파일이면 경로만 연결 (복사 안 함)
            product.overlay_image.name = norm_path[len("media/"):]
            product.save()
        else:
            with open(path, "rb") as img:
                product.overlay_image.save(filename, File(img), save=True)

        created += 1
        print(f"등록: {name} ({color}/{size})")

print(f"\n완료 - 등록 {created}개 / 건너뜀 {skipped}개")