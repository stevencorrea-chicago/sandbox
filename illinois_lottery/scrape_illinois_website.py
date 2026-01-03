# scraper_backup.py

import cloudscraper
import time
import shutil
from pathlib import Path
from bs4 import BeautifulSoup
import requests


class IllinoisLotteryScraper:
    def __init__(self, html_dir: Path, backup_dir: Path, total_pages: int):
        self.html_dir = html_dir
        self.backup_dir = backup_dir
        self.total_pages = total_pages
        self.scraper: requests.Session = cloudscraper.create_scraper()

    def backup_files(self) -> None:
        """
        Move all files from html_dir to backup_dir.
        """
        if not self.html_dir.exists() or not self.html_dir.is_dir():
            raise ValueError(f"Source directory does not exist: {self.html_dir}")

        self.backup_dir.mkdir(parents=True, exist_ok=True)

        moved_count = 0
        for item in self.html_dir.iterdir():
            if item.is_file():
                shutil.move(item, self.backup_dir / item.name)
                moved_count += 1

        print(f"Backup completed: {moved_count} files moved.")

    def scrape_pages(self) -> None:
        """
        Scrape total_pages from the Illinois Lottery website and save HTML locally.
        """
        self.html_dir.mkdir(parents=True, exist_ok=True)

        for page in range(self.total_pages):
            url = f'https://www.illinoislottery.com/dbg/results/luckydaylotto?page={page+1}'
            response = self.scraper.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            page_file = self.html_dir / f"{page+1}.html"
            with open(page_file, "w", encoding="utf-8") as f:
                for element in soup.contents:
                    f.write(str(element))

            time.sleep(1)

            if page % 100 == 0 and page > 0 :
                print(f"Scraped page {page+1}/{self.total_pages}")

    def run(self):
        """
        Run the backup and scraping sequence.
        """
        self.backup_files()
        self.scrape_pages()


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    root_path = script_path.parent
    html_dir = Path(root_path,"html_pages")
    backup_dir = Path(root_path,"html_pages_backup")
    total_pages = 1

    scraper_obj = IllinoisLotteryScraper(html_dir, backup_dir, total_pages)
    scraper_obj.run()

