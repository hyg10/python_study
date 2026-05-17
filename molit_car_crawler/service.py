from datetime import datetime

import pandas as pd
from playwright.sync_api import sync_playwright
from sqlalchemy import text

from crawler import MolitCarCrawler
from db import get_engine, init_tables
from parser import parse_excel


class MolitCarService:
    def __init__(self):
        self.engine = get_engine()
        self.crawler = MolitCarCrawler()

    def run(self) -> dict:
        init_tables()
        targets = self.crawler.list_2026_targets()
        if not targets:
            return {"files": 0, "rows": 0, "message": "2026년 자동차 등록자료 파일이 없습니다."}

        crawled_at = datetime.now()
        file_count = 0
        row_count = 0

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context(accept_downloads=True)
            page = context.new_page()
            page.goto(self.crawler.source_url, wait_until="networkidle", timeout=60_000)
            page.wait_for_timeout(1_500)

            for target in targets:
                file_path = self.crawler.download_file(target, page)
                file_record, summaries = parse_excel(
                    file_path,
                    display_name=target.display_name,
                    source_url=self.crawler.source_url,
                    crawled_at=crawled_at,
                )
                self._save_file(file_record)
                self._save_summaries(summaries, crawled_at)
                file_count += 1
                row_count += len(summaries)

                page.goto(self.crawler.source_url, wait_until="networkidle", timeout=60_000)
                page.wait_for_timeout(800)

            browser.close()

        return {
            "files": file_count,
            "rows": row_count,
            "message": f"{file_count}개 파일, {row_count}건 시도별 요약 저장 완료",
        }

    def _save_file(self, record) -> None:
        delete_sql = """
        DELETE FROM molit_car_file
        WHERE stat_year = :stat_year AND stat_month = :stat_month
        """
        insert_sql = """
        INSERT INTO molit_car_file (
            stat_year, stat_month, display_name, real_filename,
            file_size, sheet_count, source_url, crawled_at
        ) VALUES (
            :stat_year, :stat_month, :display_name, :real_filename,
            :file_size, :sheet_count, :source_url, :crawled_at
        )
        """
        payload = {
            "stat_year": record.stat_year,
            "stat_month": record.stat_month,
            "display_name": record.display_name,
            "real_filename": record.real_filename,
            "file_size": record.file_size,
            "sheet_count": record.sheet_count,
            "source_url": record.source_url,
            "crawled_at": record.crawled_at,
        }

        with self.engine.begin() as conn:
            conn.execute(text(delete_sql), payload)
            conn.execute(text(insert_sql), payload)

    def _save_summaries(self, summaries, crawled_at: datetime) -> None:
        if not summaries:
            return

        stat_year = summaries[0].stat_year
        stat_month = summaries[0].stat_month

        delete_sql = """
        DELETE FROM molit_car_summary
        WHERE stat_year = :stat_year AND stat_month = :stat_month
        """
        insert_sql = """
        INSERT INTO molit_car_summary (
            stat_year, stat_month, region_name,
            passenger_total, van_total, truck_total, special_total,
            official_total, private_total, business_total, grand_total,
            crawled_at
        ) VALUES (
            :stat_year, :stat_month, :region_name,
            :passenger_total, :van_total, :truck_total, :special_total,
            :official_total, :private_total, :business_total, :grand_total,
            :crawled_at
        )
        """

        with self.engine.begin() as conn:
            conn.execute(
                text(delete_sql),
                {"stat_year": stat_year, "stat_month": stat_month},
            )
            for item in summaries:
                conn.execute(
                    text(insert_sql),
                    {
                        "stat_year": item.stat_year,
                        "stat_month": item.stat_month,
                        "region_name": item.region_name,
                        "passenger_total": item.passenger_total,
                        "van_total": item.van_total,
                        "truck_total": item.truck_total,
                        "special_total": item.special_total,
                        "official_total": item.official_total,
                        "private_total": item.private_total,
                        "business_total": item.business_total,
                        "grand_total": item.grand_total,
                        "crawled_at": crawled_at,
                    },
                )

    def find_files(self) -> pd.DataFrame:
        sql = """
        SELECT id, stat_year, stat_month, display_name, real_filename,
               file_size, sheet_count, crawled_at
        FROM molit_car_file
        ORDER BY stat_year DESC, stat_month DESC
        """
        return pd.read_sql(sql, self.engine)

    def find_summary(self, stat_year: int | None = None) -> pd.DataFrame:
        if stat_year:
            sql = """
            SELECT stat_year, stat_month, region_name,
                   passenger_total, van_total, truck_total, special_total,
                   official_total, private_total, business_total, grand_total,
                   crawled_at
            FROM molit_car_summary
            WHERE stat_year = %(year)s
            ORDER BY stat_month DESC, region_name
            """
            return pd.read_sql(sql, self.engine, params={"year": stat_year})

        sql = """
        SELECT stat_year, stat_month, region_name,
               passenger_total, van_total, truck_total, special_total,
               official_total, private_total, business_total, grand_total,
               crawled_at
        FROM molit_car_summary
        ORDER BY stat_year DESC, stat_month DESC, region_name
        """
        return pd.read_sql(sql, self.engine)
