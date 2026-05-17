-- mydb 데이터베이스에 테이블 생성
USE mydb;

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
);

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
);
