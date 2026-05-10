from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import pandas as pd
import shutil


class LotteryDataETL:
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

    NUMBER_COLUMNS = ["num1", "num2", "num3", "num4", "num5"]

    def __init__(self, html_folder: Path, output_folder: Path, baseline_file: Path, print_enabled: bool = False):
        self.html_folder = html_folder
        self.output_folder = output_folder
        self.baseline_file = baseline_file
        self.enabled = print_enabled

        self.output_folder.mkdir(parents=True, exist_ok=True)

        self.output_file = self.output_folder / "lottery_draws.csv"
        self.output_file_numbers = self.output_folder / "lottery_draws_numbers.csv"
        self.error_file = self.output_folder / f"errors_{self.fetch_timestamp()}.log"

        if self.baseline_file.exists():
            baseline_df = pd.read_csv(self.baseline_file, dtype=str)
            self.baseline_df = self._normalize_baseline_df(baseline_df)
        else:
            self.baseline_df = pd.DataFrame(columns=self.EXPECTED_COLUMNS)

    def _normalize_baseline_df(self, df: pd.DataFrame) -> pd.DataFrame:
        if "draw_date" not in df.columns and "date" in df.columns:
            df = df.rename(columns={"date": "draw_date"})

        if "draw_date" not in df.columns:
            raise ValueError("Baseline file must contain either 'draw_date' or 'date' column.")

        df["draw_date"] = df["draw_date"].astype(str).str.strip()
        df["draw_date"] = pd.to_datetime(
            df["draw_date"],
            format="%Y%m%d",
            errors="coerce",
        )

        if df["draw_date"].isna().any():
            df["draw_date"] = pd.to_datetime(df["draw_date"].astype(str), errors="coerce")

        if df["draw_date"].isna().any():
            raise ValueError("Baseline file contains unparseable draw dates.")

        if "draw_id" not in df.columns:
            df["draw_id"] = (
                df.groupby(df["draw_date"].dt.date).cumcount().add(1).astype(str).str.zfill(2)
            )
            df["draw_id"] = df["draw_date"].dt.strftime("%Y%m%d") + "-" + df["draw_id"]

        if "year" not in df.columns:
            df["year"] = df["draw_date"].dt.year
        if "month" not in df.columns:
            df["month"] = df["draw_date"].dt.month
        if "day" not in df.columns:
            df["day"] = df["draw_date"].dt.day

        df["draw_date"] = df["draw_date"].dt.date.astype(str)

        if "dow" in df.columns:
            df["dow"] = df["dow"].astype(str)

        for col in self.NUMBER_COLUMNS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").astype(int)
            else:
                df[col] = pd.NA

        df["num_sum"] = df[self.NUMBER_COLUMNS].sum(axis=1)
        df["even_count"] = df[self.NUMBER_COLUMNS].apply(lambda row: sum(int(n) % 2 == 0 for n in row), axis=1)
        df["odd_count"] = df[self.NUMBER_COLUMNS].apply(lambda row: sum(int(n) % 2 != 0 for n in row), axis=1)
        df["consecutive_count"] = df[self.NUMBER_COLUMNS].apply(lambda row: self.consecutive_run_count([int(n) for n in row]), axis=1)

        if "source_file" not in df.columns:
            df["source_file"] = self.baseline_file.name
        if "scrape_timestamp" not in df.columns:
            df["scrape_timestamp"] = self.fetch_timestamp()

        df = df.reindex(columns=self.EXPECTED_COLUMNS)
        df = df.astype({
            "num1": int,
            "num2": int,
            "num3": int,
            "num4": int,
            "num5": int,
            "year": int,
            "month": int,
            "day": int,
            "num_sum": int,
            "even_count": int,
            "odd_count": int,
            "consecutive_count": int,
        })
        return df

    @staticmethod
    def fetch_timestamp() -> str:
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def parse_draw_date(raw_date: str) -> datetime | None:
        normalized = raw_date.strip().replace(",", "")
        try:
            return datetime.strptime(normalized.title(), "%b %d %Y")
        except ValueError:
            try:
                return datetime.strptime(normalized, "%B %d %Y")
            except ValueError:
                return None

    @staticmethod
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

    def print_data(self, message: str) -> None:
        if self.enabled:
            print(message)

    def process_file(self, file_path: Path) -> list[dict]:
        records = []

        try:
            html_page = file_path.read_text(encoding="utf-8")
            soup = BeautifulSoup(html_page, "html.parser")

            for day_sequence in range(1, 11):
                dow_tag = soup.find("span", attrs={"data-test-id": f"draw-result-info-day-{day_sequence}"})
                date_tag = soup.find("span", attrs={"data-test-id": f"draw-result-info-date-{day_sequence}"})

                if not dow_tag or not date_tag:
                    continue

                draw_date = self.parse_draw_date(date_tag.get_text(strip=True))
                if not draw_date:
                    self.print_data(f"Unable to parse date in {file_path.name}: {date_tag.get_text(strip=True)}")
                    continue

                numbers = []
                for lotto_num in range(5):
                    div = soup.find("div", id=f"result-line-primary-{lotto_num}-{day_sequence}")
                    if div and div.get_text(strip=True).isdigit():
                        numbers.append(int(div.get_text(strip=True)))

                if len(numbers) != 5:
                    continue

                numbers = sorted(numbers)
                record = {
                    "draw_id": f"{draw_date.strftime('%Y%m%d')}-{day_sequence:02d}",
                    "draw_date": draw_date.date().isoformat(),
                    "year": draw_date.year,
                    "month": draw_date.month,
                    "day": draw_date.day,
                    "dow": dow_tag.get_text(strip=True),
                    "num1": numbers[0],
                    "num2": numbers[1],
                    "num3": numbers[2],
                    "num4": numbers[3],
                    "num5": numbers[4],
                    "num_sum": sum(numbers),
                    "even_count": sum(1 for n in numbers if n % 2 == 0),
                    "odd_count": sum(1 for n in numbers if n % 2 != 0),
                    "consecutive_count": self.consecutive_run_count(numbers),
                    "source_file": file_path.name,
                    "scrape_timestamp": self.fetch_timestamp(),
                }
                records.append(record)

        except Exception as exc:
            self.print_data(f"Error processing {file_path.name}: {exc}")

        return records

    def process_all_files(self) -> pd.DataFrame:
        files = sorted([path for path in self.html_folder.iterdir() if path.is_file() and path.suffix == ".html"])
        new_records = []

        for html_file in files:
            new_records.extend(self.process_file(html_file))

        if not new_records:
            self.print_data("No new records were extracted from HTML files.")
            return pd.DataFrame(columns=self.EXPECTED_COLUMNS)

        new_df = pd.DataFrame(new_records)
        new_df = new_df.astype({
            "num1": int,
            "num2": int,
            "num3": int,
            "num4": int,
            "num5": int,
            "year": int,
            "month": int,
            "day": int,
            "num_sum": int,
            "even_count": int,
            "odd_count": int,
            "consecutive_count": int,
        })

        combined = pd.concat([self.baseline_df, new_df], ignore_index=True, sort=False)
        combined = combined.drop_duplicates(subset=["draw_date", "num1", "num2", "num3", "num4", "num5"])
        combined = combined.reindex(columns=self.EXPECTED_COLUMNS)
        combined = combined.sort_values(by=["draw_date", "draw_id"]).reset_index(drop=True)

        self.write_outputs(combined)
        return combined

    def write_outputs(self, combined: pd.DataFrame) -> None:
        combined.to_csv(self.output_file, index=False)
        combined[self.NUMBER_COLUMNS].to_csv(self.output_file_numbers, index=False, header=True)

        if self.baseline_file.exists():
            backup_file = self.baseline_file.parent / f"baseline_backup_{self.fetch_timestamp()}.csv"
            shutil.copy2(self.baseline_file, backup_file)

        self.baseline_file.parent.mkdir(parents=True, exist_ok=True)
        combined.to_csv(self.baseline_file, index=False)


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    root_path = script_path.parent

    html_folder = root_path / "html_pages"
    output_folder = root_path / "output"
    baseline_file = root_path / "input" / "baseline.csv"

    processor = LotteryDataETL(html_folder, output_folder, baseline_file, print_enabled=False)
    processor.process_all_files()
