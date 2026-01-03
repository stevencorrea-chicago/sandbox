from scrape_illinois_website import IllinoisLotteryScraper
from create_number_pool import NumberPoolGenerator
from extract_nums import HtmlProcessor
from pathlib import Path
import datetime, os

def get_current_date() -> str:
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d-%H%M%S")

def log_generated_numbers(generator: NumberPoolGenerator, generated_nums: Path, mode: str) -> None:
    with open(generated_nums, mode, encoding="utf-8") as f:
        for _ in range(5):
            new_combo = generator.generate_filtered_combination()
            latest_file = NumberPoolGenerator.determine_latest_csv_file(output_folder)
            df = generator.load_historical_draws(latest_file)
            result = generator.contains_tuple(df, new_combo)
            date_time_string = f"Numbers generated on {get_current_date()}: "
            if result:
                print(f"{date_time_string} {new_combo} (Generated combination already exists in historical draws!)")
                f.write(f"{date_time_string} {new_combo} (Generated combination already exists in historical draws!)\n")
            else:
                print(f"{date_time_string} {new_combo}")
                f.write(f"{date_time_string} {new_combo}\n")
                    
        

def menu():
    print ("Make a selection:")
    print("\t1. Scrape Illinois Lottery Website")
    print("\t2. Generate numbers")
    print("\t3. All of the above")
    print("\t4. Exit")

    user_selection = input("Selection: ")

    if not user_selection in ['1', '2', '3', '4']:
        print ("Invalid selection.")
        menu()

    if user_selection == '4':
        exit()

    return user_selection

if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    root_path = script_path.parent
    html_folder = Path(root_path, "html_pages")
    output_folder = Path(root_path, "output")
    baseline_file = Path(root_path, "input/baseline.csv")
    html_dir = Path(root_path, "html_pages")
    backup_dir = Path(root_path, "html_pages_backup")
    generated_nums = Path(root_path, "output/generated_nums.csv")

    menu_selction = menu()

    if menu_selction != '4':
        user_selection = input("How many pages should I scrape? ")
        total_pages = int(user_selection) if user_selection.isdigit() else 1

        # Scrape Illinois Lottery website
        scraper_obj = IllinoisLotteryScraper(html_dir, backup_dir, total_pages)
        scraper_obj.run()

    if menu_selction == '2' or menu_selction == '3':
        # Process HTML files and extract values from webpages
        processor = processor = HtmlProcessor(html_folder, output_folder, baseline_file, print_enabled=False)
        processor.process_all_files()

        # Generate number pool
        generator = NumberPoolGenerator(processor.output_file_without_date)

        if not os.path.exists(generated_nums):
            log_generated_numbers(generator, generated_nums, "w")
        else:
            log_generated_numbers(generator, generated_nums, "a")