# main.py
from fastapi import FastAPI, Depends, HTTPException
from typing import List, Optional

from BookRepository..book_record import BookRecord
from .book_repository import BookRepository
from .book_service import BookService
from .config.bookInventory import list_of_books
from schemas import BookCreate, BookRead
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Books API")

# --------------------------------------------------
# CORS for React Dev Server
# --------------------------------------------------
origins = [
    "http://localhost:3000",   # React dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Allowed origins
    allow_credentials=True,
    allow_methods=["*"],          # GET, POST, DELETE, etc.
    allow_headers=["*"],          # Authorization, Content-Type, etc.
)
# --------------------------------------------------
# Dependency wiring
# --------------------------------------------------
def get_repository():
    repo = BookRepository("books.db")
    # Load initial data once (idempotent due to INSERT OR IGNORE)
    repo.load_books(list_of_books)
    return repo

def get_service(repo: BookRepository = Depends(get_repository)):
    return BookService(repo)

# --------------------------------------------------
# CRUD endpoints
# --------------------------------------------------

@app.get("/books", response_model=List[BookRead])
def get_all_books(
    service: BookService = Depends(get_service)
):
    books = service.repository.get_all_books()
    return [BookRead(**b.to_dict()) for b in books]


@app.post("/books", response_model=BookRead, status_code=201)
def create_book(
    book: BookCreate,
    service: BookService = Depends(get_service)
):
    record = BookRecord(
        title=book.title,
        author=book.author,
        year=book.year,
        country=book.country,
        language=book.language,
    )
    service.repository.add_book(record)
    return BookRead(**record.to_dict())


@app.delete("/books", status_code=200)
def delete_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None,
    country: Optional[str] = None,
    language: Optional[str] = None,
    service: BookService = Depends(get_service)
):
    criteria = {
        k: v for k, v in {
            "title": title,
            "author": author,
            "year": year,
            "country": country,
            "language": language,
        }.items() if v is not None
    }

    if not criteria:
        raise HTTPException(status_code=400, detail="At least one filter is required to delete books.")

    deleted = service.repository.delete_books(**criteria)
    return {"deleted": deleted}

# --------------------------------------------------
# Search endpoint (query params, still Option A style)
# --------------------------------------------------

@app.get("/books/search", response_model=List[BookRead])
def search_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None,
    country: Optional[str] = None,
    language: Optional[str] = None,
    year_operator: str = "=",
    partial_text: bool = True,
    service: BookService = Depends(get_service)
):
    results = service.search_books(
        title=title,
        author=author,
        year=year,
        country=country,
        language=language,
        year_operator=year_operator,
        partial_text=partial_text,
    )
    return [BookRead(**b.to_dict()) for b in results]