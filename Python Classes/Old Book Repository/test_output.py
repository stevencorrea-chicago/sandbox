import json
from config.bookInventory import list_of_books

def render_books_table(books):
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
        data_width = max(len(str(book.get(col, ""))) for book in books)
        col_widths[col] = max(header_width, data_width)

    # Helper to format a row
    def format_row(row_dict):
        return "| " + " | ".join(str(row_dict.get(col, "")).ljust(col_widths[col]) for col in columns) + " |"

    # Header row
    header = format_row({col: col.capitalize() for col in columns})

    # Divider row
    divider = "-" * len(header)

    # Data rows
    rows = [format_row(book) for book in books]

    # Combine everything
    table_output = "\n".join([divider, header, divider] + rows + [divider])

    return table_output

books = [book for book in list_of_books if book['author'] == 'Thomas Mann']
print(render_books_table(books))