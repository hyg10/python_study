import os
import re
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from models import DownloadTarget

load_dotenv(Path(__file__).resolve().parent / ".env")

BASE_URL = "https://stat.molit.go.kr"
DOWNLOAD_PATH = "/portal/common/downLoadFile.do"

# 2026년 + 자동차 등록자료만 (이륜차 제외)
TARGET_PATTERN = re.compile(
    r"downFile\('([^']+)','([^']+)','([^']+)','IfrFile'\)"
)
YEAR_PREFIX = "2026"
CAR_KEYWORD = "자동차"
REG_KEYWORD = "등록"
MOTORCYCLE_KEYWORD = "이륜"


class MolitCarCrawler:
    def __init__(self):
        self.source_url = os.getenv(
            "MOLIT_STAT_URL",
            (
                "https://stat.molit.go.kr/portal/cate/statMetaView.do"
                "?hRsId=58&hFormId=5498&hSelectId=5498&hPoint=00&hAppr=1"
                "&hDivEng=&oFileName=&rFileName=&midpath=&sFormId=5498"
                "&sStart=202604&sEnd=202604&sStyleNum=2&settingRadio=xlsx"
            ),
        )
        self.download_dir = Path(
            os.getenv("DOWNLOAD_DIR", "downloads")
        )
        self.download_dir.mkdir(parents=True, exist_ok=True)

    def list_2026_targets(self) -> list[DownloadTarget]:
        html = self._fetch_html()
        return self._parse_targets(html)

    def download_file(self, target: DownloadTarget, page) -> Path:
        safe_name = re.sub(r"[^\w가-힣.\-]+", "_", target.real_filename)
        save_path = self.download_dir / safe_name

        with page.expect_download(timeout=120_000) as download_info:
            page.evaluate(
                """
                (params) => {
                    const frm = document.frm;
                    frm.oFileName.value = params.oFileName;
                    frm.rFileName.value = params.rFileName;
                    frm.midpath.value = params.midpath;
                    frm.target = "_self";
                    frm.method = "GET";
                    frm.action = "/portal/common/downLoadFile.do";
                    frm.submit();
                }
                """,
                {
                    "oFileName": target.display_name,
                    "rFileName": target.real_filename,
                    "midpath": target.midpath,
                },
            )

        download = download_info.value
        download.save_as(str(save_path))
        return save_path

    def _fetch_html(self) -> str:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
                )
            )
            page.goto(self.source_url, wait_until="networkidle", timeout=60_000)
            page.wait_for_timeout(1_500)
            html = page.content()
            browser.close()
            return html

    def _parse_targets(self, html: str) -> list[DownloadTarget]:
        soup = BeautifulSoup(html, "lxml")
        results: list[DownloadTarget] = []
        seen: set[str] = set()

        for anchor in soup.select("a[onclick]"):
            onclick = anchor.get("onclick", "")
            match = TARGET_PATTERN.search(onclick)
            if not match:
                continue

            display_name, real_filename, midpath = match.groups()
            label = anchor.get_text(" ", strip=True)

            if not self._is_2026_car_registration(label, display_name):
                continue

            key = f"{display_name}|{real_filename}"
            if key in seen:
                continue
            seen.add(key)

            results.append(
                DownloadTarget(
                    display_name=display_name,
                    real_filename=real_filename,
                    midpath=midpath,
                    label=label,
                )
            )

        results.sort(key=lambda item: item.display_name)
        return results

    @staticmethod
    def _is_2026_car_registration(label: str, display_name: str) -> bool:
        text = f"{label} {display_name}"
        return (
            YEAR_PREFIX in text
            and CAR_KEYWORD in text
            and REG_KEYWORD in text
            and MOTORCYCLE_KEYWORD not in text
        )

    @staticmethod
    def build_download_url(target: DownloadTarget) -> str:
        return urljoin(BASE_URL, DOWNLOAD_PATH)
