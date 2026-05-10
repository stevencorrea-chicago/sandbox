from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

EXPECTED_COLUMNS = [
    "draw_id",
    "draw_date",
    "year",
    "month",
    "day",
    "dow",
    "num1",
    "num2",
    "num3",
    "num4",
    "num5",
    "num_sum",
    "even_count",
    "odd_count",
    "consecutive_count",
    "source_file",
    "scrape_timestamp",
]

DATE_FORMATS = [
    "%Y%m%d",
    "%Y-%m-%d",
    "%m/%d/%Y",
    "%b %d %Y",
    "%B %d %Y",
]


def parse_date(value: str) -> datetime.date:
    normalized = value.strip().replace(",", "")

    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(normalized, fmt).date()
        except ValueError:
            continue

    raise ValueError(f"Could not parse date: {value!r}")


def consecutive_run_count(numbers: list[int]) -> int:
    numbers = sorted(numbers)
    longest = 1
    current = 1

    for index in range(1, len(numbers)):
        if numbers[index] == numbers[index - 1] + 1:
            current += 1
            longest = max(longest, current)
        else:
            current = 1

    return longest


def normalize_row(row: dict[str, str], row_index: int) -> dict[str, str]:
    if "draw_date" not in row and "date" in row:
        row["draw_date"] = row["date"]

    if "draw_date" not in row:
        raise ValueError("Row is missing 'draw_date' or 'date' column")

    draw_date = parse_date(row["draw_date"])
    numbers = []
    for col in ["num1", "num2", "num3", "num4", "num5"]:
        if col not in row or row[col].strip() == "":
            raise ValueError(f"Row is missing number value for {col}")
        numbers.append(int(row[col].strip()))

    numbers = sorted(numbers)
    num_sum = sum(numbers)
    even_count = sum(1 for n in numbers if n % 2 == 0)
    odd_count = sum(1 for n in numbers if n % 2 != 0)
    consecutive_count = consecutive_run_count(numbers)

    source_file = row.get("source_file", "baseline.csv")
    scrape_timestamp = row.get("scrape_timestamp", datetime.now().strftime("%Y%m%d_%H%M%S"))
    dow = row.get("dow", draw_date.strftime("%a"))

    draw_id = row.get("draw_id")
    if not draw_id:
        draw_id = f"{draw_date.strftime('%Y%m%d')}-{row_index + 1:02d}"

    return {
        "draw_id": draw_id,
        "draw_date": draw_date.isoformat(),
        "year": str(draw_date.year),
        "month": str(draw_date.month),
        "day": str(draw_date.day),
        "dow": dow,
        "num1": str(numbers[0]),
        "num2": str(numbers[1]),
        "num3": str(numbers[2]),
        "num4": str(numbers[3]),
        "num5": str(numbers[4]),
        "num_sum": str(num_sum),
        "even_count": str(even_count),
        "odd_count": str(odd_count),
        "consecutive_count": str(consecutive_count),
        "source_file": source_file,
        "scrape_timestamp": scrape_timestamp,
    }


def main() -> None:
    root_path = Path(__file__).resolve().parent
    baseline_path = root_path / "input" / "baseline.csv"
    backup_path = root_path / "input" / f"baseline_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    if not baseline_path.exists():
        raise FileNotFoundError(f"Baseline file not found: {baseline_path}")

    with baseline_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    normalized_rows: list[dict[str, str]] = []
    for index, row in enumerate(rows):
        normalized_rows.append(normalize_row(row, index))

    normalized_rows.sort(key=lambda row: (row["draw_date"], row["draw_id"]))

    backup_path.parent.mkdir(parents=True, exist_ok=True)
    baseline_path.replace(backup_path)

    with baseline_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=EXPECTED_COLUMNS)
        writer.writeheader()
        writer.writerows(normalized_rows)

    print(f"Baseline migrated and rewritten to {baseline_path}")
    print(f"Original baseline backed up to {backup_path}")


if __name__ == "__main__":
    main()
