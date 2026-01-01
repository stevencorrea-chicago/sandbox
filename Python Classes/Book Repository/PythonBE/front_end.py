import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTextEdit, QComboBox
)
from PyQt5.QtGui import QFont

# Import your refactored backend
from book_repository import BookRepository
from book_service import BookService
from book_record import BookRecord
from config.bookInventory import list_of_books  # Your initial book data


class BookSearchUI(QWidget):
    def __init__(self, separator_text=" --- "):
        super().__init__()

        # -------------------------
        # Backend setup
        # -------------------------
        repo = BookRepository()
        repo.load_books(list_of_books)
        self.book_service = BookService(repo)

        self.separator_text = separator_text

        self.setWindowTitle("Book Inventory Search")
        self.resize(500, 400)

        # -------------------------
        # Layouts
        # -------------------------
        main_layout = QVBoxLayout()

        # Title row
        title_layout = QHBoxLayout()
        title_label = QLabel("Title:")
        self.title_input = QLineEdit()
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_input)

        # Author row
        author_layout = QHBoxLayout()
        author_label = QLabel("Author:")
        self.author_input = QLineEdit()
        author_layout.addWidget(author_label)
        author_layout.addWidget(self.author_input)

        # Year row
        year_layout = QHBoxLayout()
        year_label = QLabel("Year:")
        self.year_input = QLineEdit()
        self.year_operator = QComboBox()
        self.year_operator.addItems(["=", ">", "<"])
        year_layout.addWidget(year_label)
        year_layout.addWidget(self.year_input)
        year_layout.addWidget(self.year_operator)

        # Country row
        country_layout = QHBoxLayout()
        country_label = QLabel("Country:")
        self.country_input = QLineEdit()
        country_layout.addWidget(country_label)
        country_layout.addWidget(self.country_input)

        # Language row
        language_layout = QHBoxLayout()
        language_label = QLabel("Language:")
        self.language_input = QLineEdit()
        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_input)

        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.handle_submit)

        # Output area
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        font = QFont("Consolas")
        font.setStyleHint(QFont.Monospace)
        self.output_box.setFont(font)

        # Add all layouts to main layout
        main_layout.addLayout(title_layout)
        main_layout.addLayout(author_layout)
        main_layout.addLayout(year_layout)
        main_layout.addLayout(country_layout)
        main_layout.addLayout(language_layout)
        main_layout.addWidget(self.submit_button)
        main_layout.addWidget(self.output_box)

        self.setLayout(main_layout)

    # -------------------------
    # Submit logic
    # -------------------------
    def handle_submit(self):
        title = self.title_input.text().strip() or None
        author = self.author_input.text().strip() or None
        year = self.year_input.text().strip() or None
        country = self.country_input.text().strip() or None
        language = self.language_input.text().strip() or None
        comparison_operator = self.year_operator.currentText()

        # Call service
        books = self.book_service.search_books(
            title=title,
            author=author,
            year=year,
            country=country,
            language=language,
            year_operator=comparison_operator,
            partial_text=True
        )

        if books:
            output = self.render_books_table(books)
        else:
            output = "No matching books found."

        self.output_box.setPlainText(output)

    # -------------------------
    # Render table
    # -------------------------
    def render_books_table(self, books):
        columns = ["title", "author", "year", "country", "language"]

        # Helper to get attribute value
        def value(book: BookRecord, field):
            return str(getattr(book, field, ""))

        # Compute column widths
        col_widths = {}
        for col in columns:
            header_width = len(col.capitalize())
            data_width = max(len(value(book, col)) for book in books)
            col_widths[col] = max(header_width, data_width)

        # Helper to format a row
        def format_row(book_or_header):
            return "| " + " | ".join(
                value(book_or_header, col).ljust(col_widths[col]) for col in columns
            ) + " |"

        # Header
        class Header:
            pass
        header_obj = Header()
        for c in columns:
            setattr(header_obj, c, c.capitalize())

        header = format_row(header_obj)
        divider = "-" * len(header)
        rows = [format_row(book) for book in books]

        return "\n".join([divider, header, divider] + rows + [divider])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookSearchUI(separator_text=" <==> ")
    window.show()
    sys.exit(app.exec_())
