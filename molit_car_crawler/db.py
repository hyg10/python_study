import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv(Path(__file__).resolve().parent / ".env")


def get_engine():
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    user = os.getenv("DB_USER", "student")
    password = os.getenv("DB_PASSWORD", "Student80*")
    db_name = os.getenv("DB_NAME", "mydb")

    db_url = (
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
        "?charset=utf8mb4"
    )
    return create_engine(db_url, pool_pre_ping=True)


def init_tables():
    engine = get_engine()

    file_sql = """
    CREATE TABLE IF NOT EXISTS molit_car_file (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        stat_year INT NOT NULL,
        stat_month INT NOT NULL,
        display_name VARCHAR(255) NOT NULL,
        real_filename VARCHAR(255) NOT NULL,
        file_size BIGINT NOT NULL DEFAULT 0,
        sheet_count INT NOT NULL DEFAULT 0,
        source_url TEXT,
        crawled_at DATETIME NOT NULL,
        UNIQUE KEY uq_molit_car_file_period (stat_year, stat_month)
    )
    """

    summary_sql = """
    CREATE TABLE IF NOT EXISTS molit_car_summary (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        stat_year INT NOT NULL,
        stat_month INT NOT NULL,
        region_name VARCHAR(50) NOT NULL,
        passenger_total BIGINT NOT NULL DEFAULT 0,
        van_total BIGINT NOT NULL DEFAULT 0,
        truck_total BIGINT NOT NULL DEFAULT 0,
        special_total BIGINT NOT NULL DEFAULT 0,
        official_total BIGINT NOT NULL DEFAULT 0,
        private_total BIGINT NOT NULL DEFAULT 0,
        business_total BIGINT NOT NULL DEFAULT 0,
        grand_total BIGINT NOT NULL DEFAULT 0,
        crawled_at DATETIME NOT NULL,
        UNIQUE KEY uq_molit_car_summary (stat_year, stat_month, region_name)
    )
    """

    with engine.begin() as conn:
        conn.execute(text(file_sql))
        conn.execute(text(summary_sql))
