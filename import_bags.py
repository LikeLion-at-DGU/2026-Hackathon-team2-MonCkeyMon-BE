import os
import csv
import django
import unicodedata

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.core.files import File
from products.models import Product

CSV_FILE = "bags.csv"
BAGS_DIR = "bags"

created = 0
skipped = 0

with open(CSV_FILE, encoding="utf-8-sig") as fp:
    for row in csv.DictReader(fp):
        filename = row["filename"].strip()
        path = os.path.join(BAGS_DIR, filename)

        if not os.path.exists(path):
            # 맥/윈도우 한글 인코딩 차이 대응
            found = None
            target = unicodedata.normalize("NFC", filename)
            for f in os.listdir(BAGS_DIR):
                if unicodedata.normalize("NFC", f) == target:
                    found = os.path.join(BAGS_DIR, f)
                    break
            if not found:
                print(f"파일 없음: {filename}")
                skipped += 1
                continue
            path = found

        # 이름 + 색상 + 사이즈로 제품명 구성 (색상별로 다른 제품)
        parts = [row["name"].strip()]
        if row["color"].strip():
            parts.append(row["color"].strip())
        if row["size"].strip():
            parts.append(row["size"].strip())
        display_name = " ".join(parts)

        if Product.objects.filter(name=display_name).exists():
            print(f"이미 있음: {display_name}")
            skipped += 1
            continue

        product = Product(
            name=display_name,
            gender=row["gender"].strip() or "FEMALE",
            category=row["category"].strip(),
            is_new=row["is_new"].strip().upper() == "TRUE",
            purchase_url=row["purchase_url"].strip() or None,
        )

        with open(path, "rb") as img:
            product.overlay_image.save(filename, File(img), save=False)

        product.save()
        created += 1
        print(f"등록: {display_name}")

print(f"\n완료 - 등록 {created}개 / 건너뜀 {skipped}개")