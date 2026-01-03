import sqlite3
from BookRepository.PythonBE.book_record import BookRecord

class BookRepository:
    def __init__(self, db_path="books.db"):
        self.db_path = db_path
        self._initialize_database()

    # --------------------------------------------------
    # Internal helpers
    # --------------------------------------------------
    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _initialize_database(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                title TEXT,
                author TEXT,
                year TEXT,
                country TEXT,
                language TEXT,
                UNIQUE(title, author, year)
            )
        """)

        conn.commit()
        conn.close()


    # --------------------------------------------------
    # Data loading
    # --------------------------------------------------
    def load_books(self, book_inventory):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.executemany(
            """
            INSERT OR IGNORE INTO books (title, author, year, country, language)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (b["title"], b["author"], b["year"], b["country"], b["language"])
                for b in book_inventory
            ]
        )

        conn.commit()
        conn.close()

    # --------------------------------------------------
    # Retrieval
    # --------------------------------------------------
    def get_all_books(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT title, author, year, country, language FROM books"
        )
        rows = cursor.fetchall()
        conn.close()

        return [BookRecord(*row) for row in rows]

    def get_all_authors(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("SELECT DISTINCT author FROM books")
        rows = cursor.fetchall()
        conn.close()

        return sorted(r[0] for r in rows)

    # --------------------------------------------------
    # Mutations
    # --------------------------------------------------
    def add_book(self, book: BookRecord):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO books (title, author, year, country, language)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                book.title,
                book.author,
                book.year,
                book.country,
                book.language
            )
        )

        conn.commit()
        conn.close()

    def delete_books(self, **criteria):
        if not criteria:
            return 0

        conditions = " AND ".join(f"{k} = ?" for k in criteria.keys())
        sql = f"DELETE FROM books WHERE {conditions}"

        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(sql, tuple(criteria.values()))
        affected = cursor.rowcount

        conn.commit()
        conn.close()

        return affected

    # --------------------------------------------------
    # Searching (low-level, no business rules)
    # --------------------------------------------------
    def search(self, where_clause="", params=()):
        conn = self._connect()
        cursor = conn.cursor()

        sql = """
            SELECT title, author, year, country, language
            FROM books
        """

        if where_clause:
            sql += f" WHERE {where_clause}"

        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()

        return [BookRecord(*row) for row in rows]
