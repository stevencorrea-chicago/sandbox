import sqlite3, json
from helper_functions import print_separator
from book_record import BookRecord


class Book:
    def __init__(self, book_inventory):
        self.book_inventory = book_inventory

        # --- INITIALIZATION CONNECTION (SAFE) ---
        # This connection is used ONLY for setup, not for queries.
        self._init_conn = sqlite3.connect("books.db")
        self._init_cursor = self._init_conn.cursor()

        self.reset_database()
        self.create_table()
        self.load_data()

        # Close initialization connection
        self._init_conn.close()

    # ----------------------------------------------------
    # NEW: Helper method to get a fresh connection per call
    # ----------------------------------------------------
    def _connect(self):
        return sqlite3.connect("books.db")

    # ----------------------------------------------------
    # Initialization methods (unchanged except cursor name)
    # ----------------------------------------------------
    def describe(self):
        conn = self._connect()
        cursor = conn.cursor()

        db_path = cursor.execute("PRAGMA database_list").fetchall()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        conn.close()
        return f"Database path: {db_path[0][2]}\nTables: {tables}\n"

    def reset_database(self):
        self._init_cursor.execute("DROP TABLE IF EXISTS books")
        self._init_conn.commit()

    def create_table(self):
        print("Creating table...")
        self._init_cursor.execute('''CREATE TABLE IF NOT EXISTS books
                            (title TEXT, author TEXT, year TEXT, country TEXT, language TEXT)''')
        self._init_conn.commit()

    def load_data(self):
        print("Loading data into the database...")
        self._init_cursor.executemany(
            'INSERT INTO books (title, author, year, country, language) VALUES (?, ?, ?, ?, ?)',
            [(book['title'], book['author'], book['year'], book['country'], book['language']) for book in self.book_inventory]
        )
        self._init_conn.commit()

    # ----------------------------------------------------
    # QUERY METHODS
    # ----------------------------------------------------
    def retrieve_all_authors(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("SELECT DISTINCT author FROM books")
        rows = cursor.fetchall()
        conn.close()

        authors = sorted({r[0] for r in rows})
        return authors if authors else "No authors were retrieved."

    def retrieve_all_books(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("SELECT title, author, year, country, language FROM books")
        rows = cursor.fetchall()
        conn.close()

        books = [
            BookRecord(r[0], r[1], r[2], r[3], r[4]) for r in rows
        ]

        return books if books else "No books were retrieved."

    def add_book(self, title, author, year, country, language):
        if not all([title, author, year, country, language]):
            return f"All fields must be filled."

        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO books (title, author, year, country, language) VALUES (?, ?, ?, ?, ?)',
            (title, author, year, country, language)
        )
        conn.commit()
        conn.close()

    def delete_book(self, **kwargs):
        if not kwargs:
            return "No parameters provided to delete a book."

        conn = self._connect()
        cursor = conn.cursor()

        if len(kwargs) == 1:
            key, value = list(kwargs.items())[0]
            sql = f"DELETE FROM books WHERE {key} = ?"
            cursor.execute(sql, (value,))
        else:
            conditions = " AND ".join([f"{k} = ?" for k in kwargs.keys()])
            sql = f"DELETE FROM books WHERE {conditions}"
            cursor.execute(sql, tuple(kwargs.values()))

        conn.commit()
        conn.close()    

    def multi_field_search(self, partial_text=True, **kwargs):
        if not kwargs:
            return "No parameters provided to perform a search."

        conn = self._connect()
        cursor = conn.cursor()

        if len(kwargs) == 1 and not partial_text:
            key, value = list(kwargs.items())[0]
            sql = f"SELECT title, author, year, country, language FROM books WHERE LOWER({key}) = LOWER(?)"
            cursor.execute(sql, (value,))
        elif len(kwargs) == 1 and partial_text:
            key, value = list(kwargs.items())[0]
            sql = f"SELECT title, author, year, country, language FROM books WHERE LOWER({key}) LIKE LOWER(?)"
            cursor.execute(sql, (f"%{value}%",))
        elif 'year' in kwargs.keys() and len(kwargs) == 2 and 'year_operator' in kwargs:
            value = kwargs.get('year')
            operator = kwargs.get('year_operator', '=')
            sql = f"""
                    SELECT title, author, year, country, language 
                    FROM books 
                    WHERE CAST(year AS INTEGER) {operator} CAST(? AS INTEGER)
                    ORDER BY CAST(year AS INTEGER) DESC
                    """
            cursor.execute(sql, (f"{value}",))
        elif len(kwargs) > 1 and not partial_text:
            conditions = " AND ".join([f"{k} = LOWER(?)" for k in kwargs.keys()])
            sql = f"SELECT title, author, year, country, language FROM books WHERE LOWER({conditions})"
            cursor.execute(sql, tuple(kwargs.values()))
        else:
            conditions = " AND ".join([f"LOWER({k}) LIKE LOWER(?)" for k in kwargs.keys()])
            sql = f"SELECT title, author, year, country, language FROM books WHERE {conditions}"
            cursor.execute(sql, tuple([f"%{v}%" for v in kwargs.values()]))


        rows = cursor.fetchall()
        conn.close()

        books = [ BookRecord(r[0], r[1], r[2], r[3], r[4]) for r in rows ]
        
        no_books_found_message = {"Result": f"No books found using the provided search criteria.", "Search Criteria": kwargs}
        return books if books else no_books_found_message

def main():
    from config.bookInventory import list_of_books
    book_class = Book(list_of_books)

    print(json.dumps(book_class.multi_field_search(partial_text=True, country="united s"), ensure_ascii=True, indent=2))
    


    exit (0)

    print_separator("Book by partial title")
    print(json.dumps(book_class.book_by_title("Grass", partial_text=True), ensure_ascii=False, indent=2))
    print_separator("Book by exact title")
    print(json.dumps(book_class.book_by_title("Pedro Páramo", partial_text=False), ensure_ascii=False, indent=2))
    print_separator("Book by year")
    print(json.dumps(book_class.book_by_year(1959), indent=2))    
    print_separator("Book by exact author name")
    print(json.dumps(book_class.book_by_author("Rumi", partial_text=False), ensure_ascii=False, indent=2))
    print_separator("Book by partial author name")
    print(json.dumps(book_class.book_by_author("Orw", partial_text=True), ensure_ascii=False, indent=2))
    print_separator("Book by exact country name")
    print(json.dumps(book_class.book_by_country("India", partial_text=False), ensure_ascii=False, indent=2))
    print_separator("Book by partial Country name")
    print(json.dumps(book_class.book_by_country("Bel", partial_text=True), ensure_ascii=False, indent=2))
    print_separator("Book by exact language")
    print(json.dumps(book_class.book_by_language("Sanskrit", partial_text=False), ensure_ascii=False, indent=2))
    print_separator("Book by partial language")
    print(json.dumps(book_class.book_by_language("span", partial_text=True), ensure_ascii=False, indent=2))
    print_separator("Retrieve all authors")
    print(json.dumps(book_class.retrieve_all_authors(), ensure_ascii=False, indent=2))
    
if __name__ == "__main__":
    main()