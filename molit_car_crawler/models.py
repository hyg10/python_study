from dataclasses import dataclass
from datetime import datetime


@dataclass
class DownloadTarget:
    display_name: str
    real_filename: str
    midpath: str
    label: str


@dataclass
class CarFileRecord:
    stat_year: int
    stat_month: int
    display_name: str
    real_filename: str
    file_size: int
    sheet_count: int
    source_url: str
    crawled_at: datetime


@dataclass
class CarSummaryRecord:
    stat_year: int
    stat_month: int
    region_name: str
    passenger_total: int
    van_total: int
    truck_total: int
    special_total: int
    official_total: int
    private_total: int
    business_total: int
    grand_total: int
