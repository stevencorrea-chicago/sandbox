# process_html.py

from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import pandas as pd
import shutil


class HtmlProcessor:
    def __init__(self, html_folder: Path, output_folder: Path, baseline_file: Path, print_enabled: bool = False):
        self.html_folder = html_folder
        self.output_folder = output_folder
        self.baseline_file = baseline_file
        self.enabled = print_enabled

        # Generate timestamped output file paths
        self.output_file_with_date = output_folder / f"{self.fetch_timestamp()}_with_date.csv"
        self.output_file_without_date = output_folder / f"{self.fetch_timestamp()}_without_date.csv"
        self.error_file = output_folder / f"errors_{self.fetch_timestamp()}.csv"

        self.output_folder.mkdir(parents=True, exist_ok=True)

        expected_cols = ["dow", "date", "num1", "num2", "num3", "num4", "num5"]

        # Load baseline if it exists, otherwise initialize empty
        if baseline_file.exists():
            self.baseline_df = pd.read_csv(baseline_file, index_col=False)
        else:
            self.baseline_df = pd.DataFrame(columns=expected_cols)


    @staticmethod
    def fetch_numerical_month(month: str) -> str:
        month_dict = {
            'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06',
            'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
        }
        return month_dict.get(month.upper(), '00')
    
    @staticmethod
    def fetch_timestamp() -> str:
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def print_data(self, data: str):
        if self.enabled:
            print(data)

    def process_file(self, file_path: Path) -> list[dict]:
        """
        Extract lotto results from a single HTML file.
        Returns a list of dict records: {dow, date, num1..num5}
        """
        records = []
        try:
            with file_path.open('r', encoding='utf-8') as f:
                html_page = f.read()

            soup = BeautifulSoup(html_page, "html.parser")

            for day_sequence in range(1, 11):  # check 10 results per page
                try:
                    dow = soup.find("span", attrs={"data-test-id": f"draw-result-info-day-{day_sequence}"}).get_text(strip=True)
                    date = soup.find("span", attrs={"data-test-id": f"draw-result-info-date-{day_sequence}"}).get_text(strip=True)

                    month_str, day_str, year = date.replace(",", "").split()
                    month = self.fetch_numerical_month(month_str)
                    day = day_str.zfill(2)
                    new_date = f"{year}{month}{day}"

                    self.print_data(f"{dow}, {new_date}")

                    numbers = []
                    for lotto_num in range(5):
                        div = soup.find("div", id=f"result-line-primary-{lotto_num}-{day_sequence}")
                        if div:
                            numbers.append(div.get_text(strip=True))

                    if len(numbers) == 5:
                        record = {
                            "dow": dow[:3],
                            "date": new_date,
                            "num1": numbers[0],
                            "num2": numbers[1],
                            "num3": numbers[2],
                            "num4": numbers[3],
                            "num5": numbers[4]
                        }
                        records.append(record)

                except Exception:
                    continue  # Skip malformed sequence

        except Exception as e:
            self.print_data(f"Error reading {file_path}: {e}")

        
        return records

    def process_all_files(self):
        """
        Process all HTML files, compare with baseline, and output new records only.
        """
        files = sorted([f for f in self.html_folder.iterdir() if f.is_file() and f.suffix == '.html'])
        new_records = []

        for file in files:
            new_records.extend(self.process_file(file))

        # Convert to DataFrame
        new_df = pd.DataFrame(new_records)
        
        if not new_df.empty:
            expected_cols = ["dow", "date", "num1", "num2", "num3", "num4", "num5"]

            # Normalize new data
            new_df = new_df.reindex(columns=expected_cols).fillna("").astype(str)
            
            # Combine with baseline and remove duplicates
            combined = pd.concat([self.baseline_df, new_df], ignore_index=True)
            combined = combined.drop_duplicates(subset=expected_cols)
            
            # Sort & normalize combined for consistency
            combined = combined.reindex(columns=expected_cols).fillna("").astype(str)
            combined = combined.sort_values(by="date")
            
            # Write outputs
            combined.to_csv(self.output_file_with_date, index=False)
            combined.drop(columns=["dow", "date"]).to_csv(
                self.output_file_without_date,
                index=False,
                header=False
            )
            destination_path = self.baseline_file.parent / f"baseline_backup_{self.fetch_timestamp()}.csv"

            if self.baseline_file.exists():
                shutil.copy2(self.baseline_file, destination_path)
                self.baseline_file.unlink()
                combined.to_csv(self.baseline_file, index=False)


if __name__ == "__main__":
    # Get the absolute path to the current script
    script_path = Path(__file__).resolve()
    root_path = script_path.parent

    html_folder = Path(root_path, "html_pages")
    output_folder = Path(root_path, "output")
    baseline_file = Path(root_path, "input/baseline.csv")

    processor = HtmlProcessor(html_folder, output_folder, baseline_file, print_enabled=False)
    processor.process_all_files()
