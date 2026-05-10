# scraper_backup.py

import cloudscraper
import time
import shutil
from pathlib import Path
from bs4 import BeautifulSoup
import requests


class IllinoisLotteryScraper:
    def __init__(self, html_dir: Path, backup_dir: Path, total_pages: int, delay_seconds: float = 1.0):
        self.html_dir = html_dir
        self.backup_dir = backup_dir
        self.total_pages = total_pages
        self.delay_seconds = delay_seconds
        self.scraper: requests.Session = cloudscraper.create_scraper()

    def backup_files(self) -> None:
        """Archive any existing HTML files before scraping new pages."""
        if not self.html_dir.exists():
            return

        self.backup_dir.mkdir(parents=True, exist_ok=True)
        moved_count = 0

        for item in self.html_dir.iterdir():
            if item.is_file():
                item.rename(self.backup_dir / item.name)
                moved_count += 1

        if moved_count:
            print(f"Backup completed: {moved_count} files moved.")

    def scrape_pages(self) -> None:
        """Scrape lottery pages and persist raw HTML files."""
        self.html_dir.mkdir(parents=True, exist_ok=True)

        for page in range(1, self.total_pages + 1):
            url = f"https://www.illinoislottery.com/dbg/results/luckydaylotto?page={page}"
            response = self.scraper.get(url, timeout=30)
            response.raise_for_status()

            page_file = self.html_dir / f"{page}.html"
            page_file.write_text(response.text, encoding="utf-8")

            if page % 100 == 0:
                print(f"Scraped page {page}/{self.total_pages}")

            time.sleep(self.delay_seconds)

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

