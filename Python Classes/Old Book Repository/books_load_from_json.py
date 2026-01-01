from config.bookInventory import list_of_books
import json


def print_separator(text):
    total_length = 80
    length_of_asterisks = (total_length - len(text) - 2) // 2
    print("*" * length_of_asterisks + f" {text.upper()} " + "*" * length_of_asterisks)

class Book:
    def __init__(self, book_inventory):
        # if not isinstance(book_inventory, dict):
        #     raise TypeError("Expected a dictionary")
        self.book_inventory = book_inventory

    def describe(self):     
        return f"There are {len(self.book_inventory)} books listed in our book catalog."
    
    def book_by_title(self, title, partial_text=False):
        books_by_title = {}
        
        for book in self.book_inventory:
            if book["title"].upper() == title.upper() and not partial_text:
                books_by_title[book["title"]] = book
            elif title.upper() in book["title"].upper() and partial_text:
                books_by_title[book["title"]] = book
        
        return books_by_title if books_by_title else "No books found for the given title."

    
    def book_by_year(self, year):
        books_by_year = {}
    
        for book in self.book_inventory:
            if book["year"] == year:
                books_by_year[book["title"]] = book
        
        return books_by_year if books_by_year else "No books found for the given year."
    
    def book_by_author(self, author, partial_text=False):
        books_by_author = {}
    
        for book in self.book_inventory:
            if book["author"].upper() == author.upper() and not partial_text:
                books_by_author[book["title"]] = book
            elif author.upper() in book["author"].upper() and partial_text:
                books_by_author[book["title"]] = book
        
        return books_by_author if books_by_author else "No books found for the given author."

    def book_by_country(self, country, partial_text=False):
        books_by_country = {}
    
        for book in self.book_inventory:
            if book["country"].upper() == country.upper() and not partial_text:
                books_by_country[book["title"]] = book
            elif country.upper() in book["country"].upper() and partial_text:
                books_by_country[book["title"]] = book
        
        return books_by_country if books_by_country else "No books found for the given country."
    
    def book_by_language(self, language, partial_text=False):
        books_by_language = []
    
        for book in self.book_inventory:
            if book["language"].upper() == language.upper() and not partial_text:
                books_by_language.append(book)
            elif language.upper() in book["language"].upper() and partial_text:
                books_by_language.append(book)
        
        return books_by_language if books_by_language else "No books found for the given language."    

    def retrieve_all_authors(self):
        authors = set()
    
        for book in self.book_inventory:
            authors.add(book["author"]) 
            
        return sorted(authors) if authors else "No authors were retrieved."
    
    def print_list_items(self, list_of_items):
        for item in list_of_items:
            print(item)

book_class = Book(list_of_books)
print(book_class.describe())
print_separator("Book by partial title")
print(json.dumps(book_class.book_by_title("Grass", partial_text=True), ensure_ascii=False, indent=2))
print_separator("Book by exact title")
print(json.dumps(book_class.book_by_title("Pedro Páramo", partial_text=False), ensure_ascii=False, indent=2))
print_separator("Book by year")
print(json.dumps(book_class.book_by_year(1959), indent=2))    
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
print_separator("Print all authors")
book_class.print_list_items(book_class.retrieve_all_authors())