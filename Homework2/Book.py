class Book:
    

    def __init__(self, title, author, page_count, isbn):
        self.title = title
        self.author = author
        self.page_count = page_count
        self.isbn = isbn  


    def __str__(self):
        return f"{self.title} - {self.author} ({self.page_count} pages, ISBN: {self.isbn})"    