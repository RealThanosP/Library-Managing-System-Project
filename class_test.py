class User:
    '''Creates a user that can interact with the library'''
    def __init__(self, name, password):
        self.name = name
        self.password = password
        credentials = [self.name, self.password]


    def sign_in(self, name, password):
        if name == self.name and password == self.password:
            #Open another window with access to the library
            pass

    def loan_out(self, book):
        return #To do

    def return_in(self, book):
        return #To do


class Book:
    '''Defines the books with their attributes'''
    #Attributes of the book:
    def __init__(self, isbn, title, author,stock=0):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.stock = stock

    def __repr__(self):
        return f"({self.isbn}, {self.title}, {self.author}, {self.stock})"


class Library:
    def __init__(self, books):
        self.books = []

    def __repr__(self):
        return f"{self.books}"

    def update(self):
        #Loads up the new library from a database.txt to a list self.books
        with open("database.txt", "r", encoding="utf-8") as database:
            for line in database:
                line = line.strip().split("\t")
                if line == [""]: continue
            #Defines the attributes of the book on the line
                isbn = line[0]
                title = line[1]
                author = line[2]
                stock = line[3]
                book = Book(isbn, title, author, stock)
                self.books.append(book)
        return self.books

    def add_book(self, book):
        #Adds a book to the database.txt and the list books of the library
        if isinstance(book, Book):
            with open("database.txt", "a", encoding="utf-8") as database:
                attributes = [str(book.isbn), book.title, book.author, str(book.stock)]
                book_str = "\t".join(attributes) + "\n"#The book attributes in a line seperated by tab spaces

            #Adds a new book only when it's not in the database
                if str(book) in str(self.books): pass
                else: database.write(book_str)

    def remove_book(self):
        return #To do??? IDK if it's going to be useful.I mean a good library is a big library right?


    def add_stock(self, book):
        return #To do

    def sub_stock(self, book):
        return #To do

    def find(self, book):
        return #To do

def ask_book():
    user_input = input("Enter book attributes seperated by tabs(isbn, title, author, stock): ")
    user_input = user_input.strip(" ").split("\t")
    book = Book(user_input[0], user_input[1], user_input[2], user_input[3])
    return book

def main():
    library = Library([])
    library.update()
    library.add_book(ask_book())
    library.update()
    print(library)


if __name__ == "__main__":
    main()









