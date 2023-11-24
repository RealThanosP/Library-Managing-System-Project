class Book:
    def __init__(self, isbn, title, author, summary = "Summary: ", stock=0):
        self.title = str(title)
        self.isbn = int(isbn)
        self.author = author
        self.summary = summary
        self.stock = int(stock)
 
    def add_summary(self, summary):
        self.summary = summary

    def add_stock(self, new_pieces):
        self.stock += new_pieces

class Library:
    def __init__(self, books):
        self.books = {}

    def book_loading(self):
        #Loads a dictionary from the database.txt
        database = open("LMS-Project/Code Ideas/database.txt", "r", encoding="utf-8")
        for line in database:
            line = line.strip().split("(|)")
            #Adds new elements to the dictionary:
            self.books = {**self.books, **{int(line[0]):line[1:]}}
        database.close()

    def is_in_Library(self, book):
        #Atribute: book, must be a class:Book object
        #Checks if a book object is in library
        if book.isbn not in self.books:
            return False
        else:
            return True
        
    def add_new_book(self):
        try:
        #Asks for inputs from the user
            isbn = int(input("Enter isbn: "))
            title = input("Enter book-title: ")
            author = input("Enter the author: ")
            summary = input("Enter a summary: ")
            stock = int(input("Enter the pieces left: "))       
        except ValueError:
            print("The isbn or the total stock inputs are invalid, Try again: ")
        
        try:
            atributes = [isbn, title, author, summary, stock]
            book = ",".join(atributes)

        #Adds the attributes of the book, seperated by commas 
            database = open("LMS-Project/Code Ideas/database.txt", "a", encoding="utf-8")
            database.write(book)
            database.close()
            
        except UnboundLocalError:
            return
        
class User:
    admin_password = "library123"
    def __init__(self, name="", admin_access=False):
        self.name = name
        self.admin_access = admin_access
    
    def is_admin(self, name, password):
        name = input("Enter a name: ")
        password = input("Enter password: ")
        if name == "admin":
            if password == self.admin_password:
                self.name = name
                self.admin_access = True
        else:
            self.name = name





    








