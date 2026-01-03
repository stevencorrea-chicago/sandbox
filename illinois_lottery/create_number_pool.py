# create_number_pool.py

import random
from pathlib import Path
from datetime import datetime
import pandas as pd

class NumberPoolGenerator:
    def __init__(self, filepath: Path):
        self.historical_draws = self.load_draws_from_file(filepath)
    
    @staticmethod
    def load_draws_from_file(filepath: Path):
        draws = set()
        with open(filepath, 'r') as f:
            for line in f:
                parts = [int(num) for num in line.strip().split(',') if num.strip().isdigit()]
                if len(parts) == 5:
                    draws.add(tuple(sorted(parts)))
        return draws

    @staticmethod
    def is_unusual_pattern(numbers):
        """Apply filters to reject patterns that are extremely rare or overly common."""
        numbers = sorted(numbers)

        # 4+ consecutive numbers
        consecutive = 1
        for i in range(1, len(numbers)):
            if numbers[i] == numbers[i - 1] + 1:
                consecutive += 1
                if consecutive >= 4:
                    return True
            else:
                consecutive = 1

        # All even or all odd
        evens = sum(1 for n in numbers if n % 2 == 0)
        if evens == 0 or evens == len(numbers):
            return True

        # All from the same decade (e.g., 30s)
        decades = set(n // 10 for n in numbers)
        if len(decades) == 1:
            return True

        # All ending in same digit (e.g., 5, 15, 25, ...)
        endings = set(n % 10 for n in numbers)
        if len(endings) == 1:
            return True

        # Sum of numbers too low or too high
        total = sum(numbers)
        if total < 80 or total > 160:
            return True

        return False

    def generate_filtered_combination(self):
        """Generate a new 5-number combo avoiding known patterns and past results."""
        while True:
            combination = tuple(sorted(random.sample(range(1, 46), 5)))
            if combination in self.historical_draws:
                continue
            if self.is_unusual_pattern(combination):
                continue
            return combination

    @staticmethod
    def determine_latest_csv_file(directory: Path) -> Path:
        csv_files = list(directory.glob("*_without_date.csv"))
        if not csv_files:
            raise FileNotFoundError("No CSV files found in the specified directory.")
        latest_file = max(csv_files, key=lambda f: f.stat().st_mtime)
        return latest_file
    
    def load_historical_draws(self, filepath: Path):
        df = pd.read_csv(filepath, header=None)
        df.sort_values(by=[0, 1, 2, 3, 4], inplace=True)  # type: ignore
        return df

    @staticmethod
    def contains_tuple(df: pd.DataFrame, values: tuple) -> bool:
        """
        Check if a DataFrame contains a row matching the given tuple.
        
        Parameters:
        df (pd.DataFrame): The DataFrame to search.
        values (tuple): A tuple of values (must match DataFrame column order).
        
        Returns:
        bool: True if the row exists, False otherwise.
        """
        # Convert tuple to a DataFrame row for comparison
        row = pd.DataFrame([values], columns=df.columns)
        
        # Check if any row in df matches
        return ((df == row.iloc[0]).all(axis=1)).any()

def main():
    script_path = Path(__file__).resolve()
    root_path = script_path.parent
    # Get current date and time
    now = datetime.now()
    # Format as "YYYYMMDD_HHMMSS"
    date = now.strftime("%Y%m%d_%H%M%S")
    filepath = Path(root_path, f"output/{date}_without_date.csv")
    latest_file = NumberPoolGenerator.determine_latest_csv_file(Path(root_path, "output"))

    # generator = NumberPoolGenerator(filepath)
    generator = NumberPoolGenerator(latest_file)
    df = generator.load_historical_draws(latest_file)
    
    print("Historical draws loaded from:", latest_file)
    for _ in range(5):
        new_combo = generator.generate_filtered_combination()
        result = generator.contains_tuple(df, new_combo)
        if result:
            print("Generated combination already exists in historical draws:", new_combo)
        else:
            print("Generated combination:", new_combo, result)
            


if __name__ == "__main__":
    main()
