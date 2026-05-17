# molit_car_crawler

국토교통부 [국토교통 통계누리](https://stat.molit.go.kr)의 **자동차등록현황보고** 통계에서 **2026년 자동차 등록자료** xlsx만 수집하고, MySQL `mydb`에 저장하는 크롤러입니다.

> 이륜차(이륜자동차) 신고현황 통계는 수집 대상에서 제외합니다.

## 수집 대상

- **출처:** [자동차등록현황보고 (Total Registered Motor Vehicles)](https://stat.molit.go.kr/portal/cate/statMetaView.do?hRsId=58&hFormId=5498&hSelectId=5498&hPoint=00&hAppr=1&hDivEng=&oFileName=&rFileName=&midpath=&sFormId=5498&sStart=202604&sEnd=202604&sStyleNum=2&settingRadio=xlsx)
- **파일:** `2026년 N월 자동차 등록자료 통계.xlsx` 형식의 월별 엑셀
- **파싱 시트:** `01.통계표` (시도별 차종·용도별 등록 현황)

## 주요 기능

1. Playwright로 통계 페이지 접속 후 2026년 자동차 등록 xlsx 다운로드
2. `01.통계표` 시트에서 시도별 요약 데이터 추출
3. MySQL `mydb`에 파일 메타정보 및 시도별 집계 저장
4. 동일 연·월 데이터 재수집 시 기존 데이터 교체(삭제 후 삽입)

## 요구 사항

- Python 3.10+
- MySQL 8.x (또는 호환 DB)
- Chromium (Playwright 설치 시 자동 설치)

## 설치

```bash
cd molit_car_crawler

# 가상환경 (권장)
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
playwright install chromium
```

## 환경 설정

`.env.example`을 복사해 `.env` 파일을 만듭니다.

```bash
cp .env.example .env   # Windows: copy .env.example .env
```

| 변수 | 설명 | 예시 |
|------|------|------|
| `DB_HOST` | MySQL 호스트 | `localhost` |
| `DB_PORT` | MySQL 포트 | `3306` |
| `DB_USER` | DB 사용자 | `student` |
| `DB_PASSWORD` | DB 비밀번호 | (본인 환경 값) |
| `DB_NAME` | 데이터베이스명 | `mydb` |
| `MOLIT_STAT_URL` | 통계 페이지 URL | (기본값 사용 가능) |
| `DOWNLOAD_DIR` | xlsx 임시 저장 경로 | `downloads` |

> `.env`는 비밀번호가 포함되므로 **Git에 커밋하지 마세요.**

## DB 준비

MySQL에서 `mydb` 데이터베이스를 만든 뒤, 아래 중 하나로 테이블을 생성합니다.

```bash
# Python으로 생성
python main.py init
```

또는 `dbscript.sql`을 직접 실행합니다.

```sql
mysql -u student -p < dbscript.sql
```

## 사용법

```bash
# 1) 테이블 생성 (최초 1회)
python main.py init

# 2) 크롤링 + DB 저장
python main.py crawl

# 3) 저장된 파일 목록 조회
python main.py list-files

# 4) 시도별 요약 데이터 조회
python main.py list-summary --year 2026
```

### CLI 명령

| 명령 | 설명 |
|------|------|
| `init` | `molit_car_file`, `molit_car_summary` 테이블 생성 |
| `crawl` | 2026년 자동차 등록 xlsx 다운로드 및 DB 저장 |
| `list-files` | 저장된 파일 메타정보 출력 |
| `list-summary` | 시도별 요약 데이터 출력 (`--year` 옵션) |

## DB 스키마

### `molit_car_file`

다운로드한 월별 xlsx 파일 메타정보

| 컬럼 | 설명 |
|------|------|
| `stat_year`, `stat_month` | 통계 연·월 |
| `display_name` | 화면 표시 파일명 |
| `real_filename` | 실제 서버 파일명 |
| `file_size` | 파일 크기 (bytes) |
| `sheet_count` | 엑셀 시트 수 |
| `crawled_at` | 크롤링 시각 |

### `molit_car_summary`

`01.통계표` 시트의 시도별 등록 대수

| 컬럼 | 설명 |
|------|------|
| `region_name` | 시도명 (서울, 부산, …) |
| `passenger_total` | 승용 합계 |
| `van_total` | 승합 합계 |
| `truck_total` | 화물 합계 |
| `special_total` | 특수 합계 |
| `official_total` | 총계-관용 |
| `private_total` | 총계-자가용 |
| `business_total` | 총계-영업용 |
| `grand_total` | 총계-계 |

## 프로젝트 구조

```
molit_car_crawler/
├── main.py           # CLI 진입점
├── crawler.py        # 목록 수집 및 xlsx 다운로드
├── parser.py         # 엑셀 파싱
├── service.py        # 크롤링·저장 오케스트레이션
├── db.py             # DB 연결 및 테이블 초기화
├── models.py         # 데이터 클래스
├── dbscript.sql      # 테이블 DDL
├── requirements.txt
├── .env.example
└── downloads/        # 다운로드 임시 폴더 (git 제외)
```

## Git 업로드 시 참고

`.gitignore`에 의해 제외되는 항목:

- `.env` (DB 비밀번호)
- `downloads/` (다운로드 xlsx)
- `.venv/`, `__pycache__/`

커밋 전 확인:

```bash
git status
```

## 트러블슈팅

| 증상 | 해결 |
|------|------|
| `Can't connect to MySQL server` | MySQL 서비스 실행 및 `.env` 접속 정보 확인 |
| `2026년 파일이 없습니다` | `MOLIT_STAT_URL`이 국토교통 통계누리 URL인지 확인 |
| Playwright 오류 | `playwright install chromium` 재실행 |
| SSL 인증 오류 | 이 프로젝트는 Playwright 사용 (urllib 직접 호출 아님) |

## 데이터 출처

- 제공기관: 국토교통부
- 통계명: 자동차등록현황보고 (승인통계)
- 이용 시 [국토교통 통계누리](https://stat.molit.go.kr) 출처 표기 권장

## 관련 프로젝트

상위 저장소 `crawling_project`의 `auto_crawler`와 동일한 MySQL 연결 패턴(`SQLAlchemy` + `pymysql`)을 사용합니다.
