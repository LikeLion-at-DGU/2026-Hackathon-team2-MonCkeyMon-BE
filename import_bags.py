import os
import csv
import django
import unicodedata

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.core.files import File
from products.models import Product

CSV_FILE = "bags.csv"
BAGS_DIR = "bags" if os.path.isdir("bags") else "media/products/overlays"

created = 0
skipped = 0

with open(CSV_FILE, encoding="utf-8-sig") as fp:
    for row in csv.DictReader(fp):
        filename = row["filename"].strip()
        path = os.path.join(BAGS_DIR, filename)

        if not os.path.exists(path):
            def _norm(s):
                s = unicodedata.normalize("NFKD", s)
                s = "".join(c for c in s if not unicodedata.combining(c))
                return "".join(c for c in s if c.isalnum()).lower()

            found = None
            target = _norm(os.path.splitext(filename)[0])
            for f in os.listdir(BAGS_DIR):
                if _norm(os.path.splitext(f)[0]) == target:
                    found = os.path.join(BAGS_DIR, f)
                    break
            if not found:
                print(f"파일 없음: {filename}")
                skipped += 1
                continue
            path = found

        name = row["name"].strip()
        color = row["color"].strip()
        size = row["size"].strip()

        # 이름 + 색상 + 사이즈 조합이 같으면 중복으로 간주
        if Product.objects.filter(name=name, color=color, size=size).exists():
            print(f"이미 있음: {name} ({color}/{size})")
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

        with open(path, "rb") as img:
            product.overlay_image.save(filename, File(img), save=False)

        product.save()
        created += 1
        print(f"등록: {name} ({color}/{size})")

print(f"\n완료 - 등록 {created}개 / 건너뜀 {skipped}개")