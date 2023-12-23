import sqlite3

def create_table():
    conn = sqlite3.connect('Library.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS books(
    isbn integer ,
    title text,
    author text,
    section integer,
    stock integer,
    UNIQUE (isbn)
    UNIQUE (title, author)
    )""")
    conn.commit()
    conn.close()

def drop_table():
    conn = sqlite3.connect("Library.db")
    c = conn.cursor()
    c.execute("DROP TABLE books")
    conn.commit()
        
class Book:
    def __init__(self,isbn,title,author,section,stock):
        self.isbn = int(isbn)
        self.title = str(title)
        self.author = str(author)
        self.section = int(section)
        self.stock = int(stock)
    def __str__(self) -> str:
        return f"({self.isbn}, {self.title}, {self.author}, {self.section}, {self.stock})"

class Database:
    '''Handles all the functionalities of the database of books of the app'''
    def __init__(self, name):
        self.conn = sqlite3.connect(name)
        self.c = self.conn.cursor()

        self.conn = sqlite3.connect('Library.db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS books(
        isbn integer ,
        title text,
        author text,
        section integer,
        stock integer,
        UNIQUE (isbn) ON CONFLICT IGNORE
        )""")
        self.conn.commit()
    
    def add_book_database(self, isbn, title, author, section, stock):
        add = Book(isbn,title,author,section,stock) 
        value_to_check = add.isbn
        check_value_sql = '''
        SELECT EXISTS (
            SELECT 1
            FROM books
            WHERE isbn = ?
        ) AS value_exists
        '''
    
        self.c.execute(check_value_sql, (value_to_check,))
    
        if self.c.fetchone()[0]:
            return "This book is already in the database.\n You can edit it's details on the edit window."
        try:
            self.c.execute("INSERT INTO books  VALUES (?, ?, ?, ?, ?)",(add.isbn,add.title,add.author,add.section,add.stock))
            self.conn.commit()
            return 'Book successfully added!'
        except Exception as error:
            return "This book is already in the database.\n You can edit it's details on the edit window."

    def del_book_database(self, isbn):
        #delete records
        self.c.execute("DELETE FROM books WHERE isbn == (?)",(isbn,))
        self.conn.commit()
        return f'Book with isbn:{isbn} deleted'
        
    def show_database(self):
        self.c.execute("SELECT * FROM books ORDER by isbn")
        items = self.c.fetchall() 
        self.conn.commit()

        return items#List of tuples 

    def get_book(self, isbn, title, author):
        #show something accurate
        book_found = False
        try:
            if isbn:
                self.c.execute("SELECT * FROM books WHERE isbn == (?)", (isbn,))
                book_found = self.c.fetchall()
                
            if not book_found:
                if title and author:
                    self.c.execute("SELECT * FROM books WHERE title == (?) AND author == ?",(title, author,))
                    book_found = self.c.fetchall() 
            self.conn.commit()

            if not book_found:
                return None
            return book_found[0] #We just hope it will find only one

        except Exception as error:
            return None
    
    def checkForDublicates(self):
        self.c.execute("SELECT title,author FROM books GROUP BY title, author HAVING COUNT(*) > 1")
        dublicates = self.c.fetchall()
        self.conn.commit()

        #Checks if for the duplicate combinations of title and author found
        if dublicates: 
            return True
        return False

    def updateInfo(self, isbn, title, author, section, stock):
        edit = self.get_book(isbn, title, author)
        if edit == None:
            return "That book is not in our database.\nYou can add it on the add window"

       #Gets the rowid of the book to edit:
        self.c.execute("SELECT rowid FROM books WHERE isbn = ?", (edit[0],))
        rowid = self.c.fetchone()[0]

        try:
            self.c.execute("UPDATE books SET isbn = (?) WHERE ROWID = (?)",(isbn, rowid,))
            self.c.execute("UPDATE books SET title = (?) WHERE ROWID = (?)",(title, rowid,))
            self.c.execute("UPDATE books SET author = (?) WHERE ROWID = (?)",(author, rowid,))
            self.c.execute("UPDATE books SET section = (?) WHERE ROWID = (?)",(section, rowid,))
            self.c.execute("UPDATE books SET stock = (?) WHERE ROWID = (?)",(stock, rowid,))
            self.conn.commit()
            return "The changes were submitted successfully"

        except Exception as error:
            return "This edit is not valid\nDublicates are being created"

    def updateStock(self, title, author, new_stock):
        change = self.get_book(0, title, author)
        if change == None:
            return "That book is not in our database.\nYou can add it on the add window"

        #Gets the rowid of the book to edit:
        self.c.execute("SELECT rowid FROM books WHERE isbn = ?", (change[0],))
        rowid = self.c.fetchone()[0]

        try:
            self.c.execute("UPDATE books SET stock = (?) WHERE ROWID = (?)",(new_stock, rowid,))
            self.c.commint()
            return "The stock has benn updated"
        except Exception as error:
            return "Something went wrong, please try again"

library = Database("Library.db")
