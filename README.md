# MonCkeyMon BE

MCM 팝업/전시 키오스크용 백엔드. 방문자가 사진을 찍으면 원하는 가방·배경과 AI로 합성해 결과 이미지를 만들어주고, 관리자는 방문자 데이터를 통계로 확인할 수 있습니다.

## 주요 기능

- 상품(가방) / 배경 목록 조회, 인기 TOP3 제공
- 체험 세션(UUID) 생성 → 배경/상품 선택 → 사진 업로드 → AI 합성 이미지 생성
- OpenAI(`gpt-image-2`) 이미지 편집 API로 인물+가방+배경 합성
- 결과 공유 페이지(세션 상세) API
- 구매 링크 클릭 / 배경·상품 선택 / 좋아요 등 방문자 행동 데이터 수집
- 관리자용 통계 대시보드 API (선택 횟수, 방문자 수, 관심도 점수 등)

## 기술 스택

- Django 6 / Django REST Framework
- SQLite
- OpenAI API (이미지 합성)
- django-cors-headers
- Gunicorn, Docker
- GitHub Actions → AWS ECR/EC2(SSM) 배포

## 프로젝트 구조

| 앱 | 역할 |
| --- | --- |
| `products` | 상품(가방), 배경 모델과 목록/좋아요 API |
| `experiences` | 체험 세션 생성부터 사진 업로드, 영상 생성 요청, 상태 조회까지의 플로우 |
| `delivery` | AI 합성 이미지 생성, 결과 공유 상세 조회 |
| `analytics` | 선택/방문/관심도 등 통계 API |
| `project` | Django 설정, 최상위 URL 라우팅 |

## API

### products (`/api/`)

| Method | URL | 설명 |
| --- | --- | --- |
| GET | `/products/` | 상품 목록 (`gender`, `category`, `is_new` 필터 + TOP3) |
| GET | `/backgrounds/` | 배경 목록 (`type` 필터 + TOP3) |
| POST | `/products/<id>/like/` | 상품 좋아요 |

### experiences (`/api/experiences/`)

| Method | URL | 설명 |
| --- | --- | --- |
| POST | `/` | 체험 세션 생성 |
| PATCH | `/<session_id>/` | 배경/상품 선택 |
| POST | `/<session_id>/upload-photo/` | 인물 사진 업로드 |
| POST | `/<session_id>/generate/` | 영상 생성 요청 |
| GET | `/<session_id>/status/` | 세션 상태 조회 |
| POST | `/<session_id>/link/` | 결과 링크 수신 처리 |

### delivery (`/api/`)

| Method | URL | 설명 |
| --- | --- | --- |
| POST | `/composite/<session_id>/` | AI 합성 이미지 생성 |
| GET | `/share/<session_id>/` | 결과 공유 상세 조회 |

### analytics (`/api/analytics/`)

| Method | URL | 설명 |
| --- | --- | --- |
| GET | `/choose-count/` | 상품/배경 선택 횟수 |
| GET | `/choose-count/top5/` | 선택 횟수 TOP5 |
| GET | `/like-count/` | 상품별 좋아요 수 |
| GET | `/visitor-count/` | 전체 방문자 수 |
| GET | `/visitor-count/daily/` | 일별 방문자 수 |
| GET | `/visitor-count/today/` | 오늘 방문자 수 |
| GET | `/product-interest/` | 상품 관심도 점수(선택×1 + 링크×3 + 좋아요×5) |
| GET | `/category-session/top5/` | 카테고리별 선택 TOP5 |
| GET | `/product-session/` | 상품별 선택 횟수 목록 (`search`, `is_new` 필터 + `period=today`로 당일/누적 전환) |
| GET | `/total-link/` | 전체 링크 수신/클릭 수 |
| GET | `/today-click-count/` | 오늘 구매 링크 클릭 수 |
| GET | `/today-link-count/` | 오늘 링크 받기 수 |

## 로컬 실행

```bash
python -m venv venv
source venv/Scripts/activate   # Windows(Git Bash)
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

## 환경 변수 (`.env`)

| 변수 | 설명 | 기본값 |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Django 시크릿 키 (DEBUG=False면 필수) | - |
| `DJANGO_DEBUG` | 디버그 모드 | `True` |
| `DJANGO_ALLOWED_HOSTS` | 허용 호스트 (쉼표 구분) | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | CORS 허용 origin (쉼표 구분) | `http://localhost:3000,http://localhost:5173,https://mappingcustommoment.netlify.app` |
| `DJANGO_DB_PATH` | SQLite DB 파일 경로 | `db.sqlite3` |
| `OPENAI_API_KEY` | 이미지 합성용 OpenAI API 키 | - |

## 테스트

```bash
pip install pytest pytest-django pytest-cov
pytest
```

## 배포

`main` 브랜치에 push되면 GitHub Actions(`.github/workflows/deploy.yml`)가 Docker 이미지를 빌드해 AWS ECR에 push하고, SSM으로 EC2 인스턴스에 배포합니다.
