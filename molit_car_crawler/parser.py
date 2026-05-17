import re
from datetime import datetime
from pathlib import Path

import pandas as pd

from models import CarFileRecord, CarSummaryRecord

SUMMARY_SHEET_PREFIX = "01."
REGION_NAMES = {
    "서울",
    "부산",
    "대구",
    "인천",
    "광주",
    "대전",
    "울산",
    "세종",
    "경기",
    "강원",
    "충북",
    "충남",
    "전북",
    "전남",
    "경북",
    "경남",
    "제주",
}


def parse_year_month(value) -> tuple[int, int]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        raise ValueError("조회년월 값이 없습니다.")

    text = str(value).strip()
    match = re.search(r"(\d{4})\.(\d{1,2})", text)
    if not match:
        raise ValueError(f"조회년월 형식을 해석할 수 없습니다: {text}")

    return int(match.group(1)), int(match.group(2))


def _to_int(value) -> int:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return 0
    if isinstance(value, str):
        value = value.replace(",", "").strip()
        if not value:
            return 0
    return int(float(value))


def parse_excel(
    file_path: Path,
    *,
    display_name: str,
    source_url: str,
    crawled_at: datetime,
) -> tuple[CarFileRecord, list[CarSummaryRecord]]:
    workbook = pd.ExcelFile(file_path)
    summary_sheet = next(
        (name for name in workbook.sheet_names if name.startswith(SUMMARY_SHEET_PREFIX)),
        workbook.sheet_names[0],
    )
    frame = pd.read_excel(file_path, sheet_name=summary_sheet, header=None)

    stat_year, stat_month = parse_year_month(frame.iloc[1, 1])
    summaries: list[CarSummaryRecord] = []

    for row_idx in range(5, len(frame)):
        region = frame.iloc[row_idx, 0]
        if region is None or (isinstance(region, float) and pd.isna(region)):
            continue

        region_name = str(region).strip()
        if region_name not in REGION_NAMES:
            continue

        passenger_total = _to_int(frame.iloc[row_idx, 5])
        van_total = _to_int(frame.iloc[row_idx, 9])
        truck_total = _to_int(frame.iloc[row_idx, 13])
        special_total = _to_int(frame.iloc[row_idx, 17])
        official_total = _to_int(frame.iloc[row_idx, 18])
        private_total = _to_int(frame.iloc[row_idx, 19])
        business_total = _to_int(frame.iloc[row_idx, 20])
        grand_total = _to_int(frame.iloc[row_idx, 21])

        summaries.append(
            CarSummaryRecord(
                stat_year=stat_year,
                stat_month=stat_month,
                region_name=region_name,
                passenger_total=passenger_total,
                van_total=van_total,
                truck_total=truck_total,
                special_total=special_total,
                official_total=official_total,
                private_total=private_total,
                business_total=business_total,
                grand_total=grand_total,
            )
        )

    file_record = CarFileRecord(
        stat_year=stat_year,
        stat_month=stat_month,
        display_name=display_name,
        real_filename=file_path.name,
        file_size=file_path.stat().st_size,
        sheet_count=len(workbook.sheet_names),
        source_url=source_url,
        crawled_at=crawled_at,
    )
    return file_record, summaries
