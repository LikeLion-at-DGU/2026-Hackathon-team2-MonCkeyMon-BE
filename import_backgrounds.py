import os
import django
import unicodedata

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.core.files import File
from products.models import Background

TAGS = {
    #나라 별
    "일본": "시즈오카,후지산",
    "대한민국": "서울,남산",
    "아랍에미리트": "두바이,부르즈할리파",
    "프랑스": "파리, 에펠탑",
    "미국": "뉴욕,브루클린브리지",
    "영국": "런던,빅벤",
    "중국": "상하이,와이탄",
    "대만": "타이베이,샹산",
    "독일": "로텐부르크,마르크트광장",
    "싱가포르": "싱가포르,마리나베이샌즈",
    "캐나다": "밴프,레이크루이스",
    "하와이": "호놀룰루,와이키키",
    "홍콩": "침사추이,빅토리아하버",
    # 큐레이션룸
    "A Day with MCM - Milano": "밀라노,시티룩",
    "MCM X ATEEZ with MINGI - FIX ON": "에이티즈,민기",
    "MCM x DJ Khaled x We The Best": "DJ칼리드,컬래버",
    "Pina collection": "피나,스터드",
    "The pink edit": "핑크,파스텔",
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