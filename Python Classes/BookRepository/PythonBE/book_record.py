class BookRecord:
    def __init__(self, title, author, year, country, language):
        self.title = title
        self.author = author
        self.year = year
        self.country = country
        self.language = language

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "country": self.country,
            "language": self.language
        }

    def __str__(self):
        return f"{self.title} ({self.year}) by {self.author}"
