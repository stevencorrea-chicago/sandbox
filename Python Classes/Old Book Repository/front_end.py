import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTextEdit, QComboBox
)
from PyQt5.QtGui import QFont

class BookSearchUI(QWidget):
    def __init__(self, separator_text=" --- "):
        super().__init__()
        
        self.book_inventory = Book(list_of_books)
        self.separator_text = separator_text

        self.setWindowTitle("Book Inventory Search")
        self.resize(450, 300)

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

        # Country row
        country_layout = QHBoxLayout()
        country_label = QLabel("Country:")
        self.country_input = QLineEdit()
        country_layout.addWidget(country_label)
        country_layout.addWidget(self.country_input)

        # Year row
        year_layout = QHBoxLayout()
        year_label = QLabel("Year:")
        self.year_input = QLineEdit()
        year_layout.addWidget(year_label)
        year_layout.addWidget(self.year_input)

        # Year operator
        self.year_operator = QComboBox()
        self.year_operator.addItems(["=", ">", "<"])

        year_layout.addWidget(year_label)
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

        font = QFont("monospace")   # or "Consolas", or "monospace"
        font.setStyleHint(QFont.Monospace)
        self.output_box.setFont(font)

        # Add everything to main layout
        main_layout.addLayout(title_layout)
        main_layout.addLayout(author_layout)
        main_layout.addLayout(year_layout)
        main_layout.addWidget(self.year_operator)
        main_layout.addLayout(country_layout)
        main_layout.addLayout(language_layout)  
        main_layout.addWidget(self.submit_button)
        main_layout.addWidget(self.output_box)

        self.setLayout(main_layout)

    # -------------------------
    # Submit logic
    # -------------------------
    def handle_submit(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        year = self.year_input.text().strip()
        country = self.country_input.text().strip()
        language = self.language_input.text().strip()
        comparison_operator = self.year_operator.currentText()

        results = []
        criteria = {}        
        # Call backend methods based on filled fields

        if title:
            criteria["title"] = title
        if author:
            criteria["author"] = author
        if year or title or author or country or language:
            criteria["year"] = year
        if year and not title and not author and not country and not language:
            criteria["year"] = year
            criteria["year_operator"] = comparison_operator
        if country:
            criteria["country"] = country
        if language:
            criteria["language"] = language

        # Format returned json
        json_results = self.book_inventory.multi_field_search(partial_text=True, **criteria)
        
        if isinstance(json_results, list) and json_results:
            results.append(self.render_books_table(json_results))
        else:
            results.append("No matching books found.")

        # Combine results
        if results:
            output = self.separator_text.join(results)
        else:
            output = "No fields filled."

        # Display results
        self.output_box.setPlainText(output)

    def render_books_table(self, books):
        """
        Render a list of book dictionaries into a table-like string
        with evenly spaced columns, using | as separators and
        underscores as row dividers. Suitable for PyQt5 text widgets.
        """

        # Define the column order
        columns = ["title", "author", "year", "country", "language"]

        # Compute max width for each column
        col_widths = {}
        for col in columns:
            header_width = len(col.capitalize())
            data_width = max(len(str(book.get_title())) if col == "title" else
                             len(str(book.get_author())) if col == "author" else
                             len(str(book.get_year())) if col == "year" else
                             len(str(book.get_country())) if col == "country" else
                             len(str(book.get_language())) for book in books)
            col_widths[col] = max(header_width, data_width)

        # Helper to format a row
        def format_row(book):
            return "| " + " | ".join([
                book.title.ljust(col_widths["title"]),
                book.author.ljust(col_widths["author"]),
                book.year.ljust(col_widths["year"]),
                book.country.ljust(col_widths["country"]),
                book.language.ljust(col_widths["language"]),
            ]) + " |"


        # Header row
        header = format_row({col: col.capitalize() for col in columns})

        # Divider row
        divider = "-" * len(header)

        # Data rows
        rows = [format_row(book) for book in books]

        # Combine everything
        table_output = "\n".join([divider, header, divider] + rows + [divider])

        return table_output


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookSearchUI(separator_text=" <==> ")  # your custom separator
    window.show()
    sys.exit(app.exec_())