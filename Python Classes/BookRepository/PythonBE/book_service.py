class BookService:
    def __init__(self, repository):
        self.repository = repository

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------
    def search_books(
        self,
        *,
        title=None,
        author=None,
        year=None,
        country=None,
        language=None,
        year_operator="=",
        partial_text=True
                        ):
        conditions = []
        params = []

        # --- Text fields ---
        for field, value in {"title": title, "author": author, "country": country, "language": language}.items():
            if value:
                if partial_text:
                    conditions.append(f"LOWER({field}) LIKE LOWER(?)")
                    params.append(f"%{value}%")
                else:
                    conditions.append(f"LOWER({field}) = LOWER(?)")
                    params.append(value)

        # --- Year field ---
        if year:
            try:
                int(year)
            except ValueError:
                return []

            op = year_operator if year_operator in ("=", "<", ">", "<=", ">=") else "="
            conditions.append(f"CAST(year AS INTEGER) {op} CAST(? AS INTEGER)")
            params.append(year)

        where_clause = " AND ".join(conditions)

        return self.repository.search(
            where_clause=where_clause,
            params=tuple(params)
        )
