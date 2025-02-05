from Homework2.Book import Book


class Library:

   def __init__(self):
        self.books = []  


   def add_book(self, book):
        for existing_book in self.books:
            if existing_book.isbn == book.isbn:
                raise Exception(f"A book with this ISBN already exists: {book.isbn}")
        self.books.append(book)
        print(f"Book added: {book}")    


   def remove_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                self.books.remove(book)
                print(f"Book removed: {book}")
                return
        raise Exception(f"No book found with ISBN: {isbn}")
   
   
   def show_books(self):
        if not self.books:
            print("The library has no books.")
        else:
            print("Books in the Library:")
            for book in self.books:
                print(f"- {book}")



try:
    library = Library()

    book1 = Book("The Alchemist", "Paulo Coelho", 184, "12345")
    book2 = Book("1984", "George Orwell", 328, "67890")
    book3 = Book("Animal Farm", "George Orwell", 152, "67890")

    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)  
    
except Exception as e:
    print(f"Error: {e}")

library.show_books()

try:
    library.remove_book("12345")
    library.show_books()
except Exception as e:
    print(f"Error: {e}")              