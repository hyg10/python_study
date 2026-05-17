import argparse
import sys

from db import init_tables
from service import MolitCarService


def main() -> int:
    parser = argparse.ArgumentParser(
        description="국토교통부 2026년 자동차 등록자료 통계 크롤러"
    )
    parser.add_argument(
        "command",
        choices=["crawl", "init", "list-files", "list-summary"],
        help="실행할 명령",
    )
    parser.add_argument(
        "--year",
        type=int,
        default=2026,
        help="list-summary 조회 연도 (기본: 2026)",
    )
    args = parser.parse_args()

    if args.command == "init":
        init_tables()
        print("테이블 생성 완료: molit_car_file, molit_car_summary")
        return 0

    service = MolitCarService()

    if args.command == "crawl":
        result = service.run()
        print(result["message"])
        return 0

    if args.command == "list-files":
        df = service.find_files()
        if df.empty:
            print("저장된 파일이 없습니다.")
        else:
            print(df.to_string(index=False))
        return 0

    if args.command == "list-summary":
        df = service.find_summary(stat_year=args.year)
        if df.empty:
            print(f"{args.year}년 요약 데이터가 없습니다.")
        else:
            print(df.to_string(index=False))
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
