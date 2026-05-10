from pathlib import Path
import datetime
import os

from scrape_illinois_website import IllinoisLotteryScraper
from create_number_pool import NumberPoolGenerator
from extract_nums import LotteryDataETL

def get_current_date() -> str:
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d-%H%M%S")

def log_generated_numbers(generator: NumberPoolGenerator, generated_nums: Path, mode: str) -> None:
    with open(generated_nums, mode, encoding="utf-8") as f:
        for _ in range(5):
            new_combo = generator.generate_filtered_combination()
            df = generator.load_historical_draws()
            result = generator.contains_tuple(df, new_combo)
            date_time_string = f"Numbers generated on {get_current_date()}: "
            if result:
                print(f"{date_time_string}{new_combo} (already exists)")
                f.write(f"{date_time_string}{new_combo} (already exists)\n")
            else:
                print(f"{date_time_string}{new_combo}")
                f.write(f"{date_time_string}{new_combo}\n")


def prompt_page_count() -> int:
    user_input = input("How many pages should I scrape? ")
    return int(user_input) if user_input.isdigit() and int(user_input) > 0 else 1


def menu() -> str:
    print("Make a selection:")
    print("\t1. Scrape Illinois Lottery Website")
    print("\t2. Generate numbers from latest dataset")
    print("\t3. Scrape + ETL + Generate")
    print("\t4. Exit")

    selection = input("Selection: ").strip()
    if selection not in {"1", "2", "3", "4"}:
        print("Invalid selection.")
        return menu()
    if selection == "4":
        exit()
    return selection

def ensure_directories(paths: list[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    root_path = script_path.parent

    html_folder = Path(root_path, "html_pages")
    backup_dir = Path(root_path, "html_pages_backup")
    output_folder = Path(root_path, "output")
    baseline_file = Path(root_path, "input/baseline.csv")
    generated_nums = output_folder / "generated_nums.csv"

    ensure_directories([html_folder, backup_dir, output_folder, baseline_file.parent])

    choice = menu()
    should_scrape = choice in {"1", "3"}
    should_generate = choice in {"2", "3"}

    if should_scrape:
        total_pages = prompt_page_count()
        scraper_obj = IllinoisLotteryScraper(html_folder, backup_dir, total_pages)
        scraper_obj.run()

    if choice == "3":
        processor = LotteryDataETL(html_folder, output_folder, baseline_file, print_enabled=False)
        processor.process_all_files()

    if should_generate:
        latest_file = NumberPoolGenerator.determine_latest_csv_file(output_folder)
        generator = NumberPoolGenerator(latest_file)
        mode = "a" if generated_nums.exists() else "w"
        log_generated_numbers(generator, generated_nums, mode)