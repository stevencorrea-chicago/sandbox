# create_number_pool.py

import random
from pathlib import Path
from datetime import datetime
import pandas as pd


class NumberPoolGenerator:
    NUMBER_COLUMNS = ["num1", "num2", "num3", "num4", "num5"]

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.historical_draws = self.load_draws_from_file(filepath)

    @staticmethod
    def load_draws_from_file(filepath: Path) -> set[tuple[int, ...]]:
        df = pd.read_csv(
            filepath,
            usecols=NumberPoolGenerator.NUMBER_COLUMNS,
            dtype={col: int for col in NumberPoolGenerator.NUMBER_COLUMNS},
        )
        return {tuple(sorted(row)) for row in df.itertuples(index=False, name=None)}

    @staticmethod
    def is_unusual_pattern(numbers: tuple[int, ...]) -> bool:
        consecutive = 1
        max_run = 1
        for i in range(1, len(numbers)):
            if numbers[i] == numbers[i - 1] + 1:
                consecutive += 1
                max_run = max(max_run, consecutive)
            else:
                consecutive = 1

        if max_run >= 4:
            return True

        evens = sum(1 for n in numbers if n % 2 == 0)
        if evens == 0 or evens == len(numbers):
            return True

        decades = set(n // 10 for n in numbers)
        if len(decades) == 1:
            return True

        endings = set(n % 10 for n in numbers)
        if len(endings) == 1:
            return True

        total = sum(numbers)
        if total < 80 or total > 160:
            return True

        return False

    def generate_filtered_combination(self) -> tuple[int, ...]:
        while True:
            combination = tuple(sorted(random.sample(range(1, 46), 5)))
            if combination in self.historical_draws:
                continue
            if self.is_unusual_pattern(combination):
                continue
            return combination

    @staticmethod
    def determine_latest_csv_file(directory: Path) -> Path:
        candidates = list(directory.glob("lottery_draws*.csv"))
        if not candidates:
            raise FileNotFoundError("No lottery_draws CSV files found in the specified directory.")
        return max(candidates, key=lambda path: path.stat().st_mtime)

    @staticmethod
    def contains_tuple(df: pd.DataFrame, values: tuple[int, ...]) -> bool:
        return tuple(values) in {
            tuple(sorted(row))
            for row in df.itertuples(index=False, name=None)
        }

    def load_historical_draws(self) -> pd.DataFrame:
        return pd.read_csv(
            self.filepath,
            usecols=self.NUMBER_COLUMNS,
            dtype={col: int for col in self.NUMBER_COLUMNS},
        )


def main() -> None:
    script_path = Path(__file__).resolve()
    root_path = script_path.parent
    latest_file = NumberPoolGenerator.determine_latest_csv_file(root_path / "output")

    generator = NumberPoolGenerator(latest_file)
    df = generator.load_historical_draws()
    print("Historical draws loaded from:", latest_file)

    for _ in range(5):
        new_combo = generator.generate_filtered_combination()
        result = generator.contains_tuple(df, new_combo)
        if result:
            print("Generated combination already exists in historical draws:", new_combo)
        else:
            print("Generated combination:", new_combo)


if __name__ == "__main__":
    main()
