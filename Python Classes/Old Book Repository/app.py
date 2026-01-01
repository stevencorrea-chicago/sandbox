from flask import Flask, render_template, request
import json

from books_load_from_sqllite import Book
from config.bookInventory import list_of_books

app = Flask(__name__)

# Instantiate your backend
book_inventory = Book(list_of_books)

SEPARATOR_TEXT = " <==> "   # same as your PyQt version


@app.route("/", methods=["GET", "POST"])
def search():
    output = ""

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        year = request.form.get("year", "").strip()

        results = []

        if title:
            results.append(json.dumps(
                book_inventory.book_by_title(title, partial_text=True),
                ensure_ascii=False, indent=2
            ))

        if author:
            results.append(json.dumps(
                book_inventory.book_by_author(author, partial_text=True),
                ensure_ascii=False, indent=2
            ))

        if year:
            results.append(json.dumps(
                book_inventory.book_by_year(year, partial_text=True),
                ensure_ascii=False, indent=2
            ))

        if results:
            output = SEPARATOR_TEXT.join(results)
        else:
            output = "No fields filled."

    return render_template("search.html", output=output)


if __name__ == "__main__":
    app.run(debug=True)