import tkinter as tk
from tkinter import ttk
from database import Database, Book
from PIL import Image, ImageTk
from User import User

class BrowseLibrary:
    def __init__(self, root, username):
        self.name = username
        self.root = root
        self.root.title("Browse the library")
        self.root.geometry("1000x700")
        self.root.minsize(1000, 700)
        self.root.maxsize(1400, 900)
        #Inittialize the library
        self.library = Database("Library.db")
        self.user = User(self.name)

        #Top Frame
        self.frameTop = tk.Frame(self.root, bg="#D2B48C")
        self.frameTop.pack(fill="both")

        # Table Frame
        self.frameTable = tk.Frame(self.frameTop, bg="#D2B48C")
        self.frameTable.pack()

        #Bottom user main Frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True, fill="both")

        #Style of the table:
        self.tableStyle = ttk.Style()
        self.tableStyle.configure("Treeview", 
            highlightthickness=0, 
            bd=0, 
            font=('Calibri', 11),
            background= "#B0A090")
        self.tableStyle.configure("Treeview.Heading", 
            font=('Calibri', 13,'bold'))
        self.tableStyle.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        self.tableStyle.map("Treeview", background=[("selected", "green")])   

        #Table scrollbar:
        self.tableScroll = tk.Scrollbar(self.frameTable)
        self.tableScroll.pack(side="right", fill="y", pady=20)
        
        self.table = ttk.Treeview(self.frameTable, yscrollcommand=self.tableScroll.set)
        self.tableScroll.configure(command=self.table.yview)
        #Define the columns of the table:
        self.table["columns"] = ("ISBN", "Title", "Author", "Section", "Stock")
        
        #Format the columns:
        self.table.column("#0", width=0, stretch="NO")
        self.table.column("ISBN", width=100, minwidth=25)
        self.table.column("Title", width=400, minwidth=125)
        self.table.column("Author", width=180, minwidth=80)
        self.table.column("Section", width=100, minwidth=60)
        self.table.column("Stock", width=50, minwidth=25)

        #Create the headings
        self.table.heading("#0", text="", anchor="w")
        self.table.heading("ISBN", text="ISBN", anchor="w", command=lambda: self.sort_column("ISBN", False))
        self.table.heading("Title", text="Title", anchor="center", command=lambda: self.sort_column("Title", False))
        self.table.heading("Author", text="Author", anchor="center", command=lambda: self.sort_column("Author", False))
        self.table.heading("Section", text="Section", anchor="w", command=lambda: self.sort_column("Section", False))
        self.table.heading("Stock", text="Stock", anchor="center", command=lambda: self.sort_column("Stock", False))
        
        #Fills up the table with database data
        self.tableFill()
        self.table.pack(pady=20, fill="y")

        #Sets the background of the main frame:
        self.setBackround(self.frame, "background.png", 1900, 800)

        #Refresh button:
        self.refreshButton = tk.Button(self.frameTop, 
                                       text="⟳", 
                                       bg="#C3C3C3",
                                       border=0,
                                       padx=10,pady=10,
                                       command=self.refresh_table)
        self.refreshButton.pack()
        
        self.loanButton = tk.Button(self.frame,
                                    text="Loan Selected",
                                    font=("Helvetica", 20),
                                    padx=15, pady=15,
                                    border=0,
                                    bg="#C3C3C3",
                                    command=self.loan_book)
        self.loanButton.place(relx=0.2, rely=0.2)

        #Error label
        self.errorLabel = tk.Label(self.frame, text="", bg="#D2B48C")
        self.errorLabel.place(relx=0.5, rely=0.9, anchor="s")

    def tableFill(self):
        '''Fills up the table with the values from the database'''
        book_list = self.library.show_database()

        for book in book_list:
            self.table.insert("", "end", value=book)

    def sort_column(self, column, reverse):
        if column in ("Stock", "ISBN", "Section"):
            data = [(int(self.table.set(child, column)), child) for child in self.table.get_children("")]
            data.sort(reverse=reverse)
        else:
            data = [(self.table.set(child, column), child) for child in self.table.get_children("")]
            data.sort(reverse=reverse)

        for index, (val, child) in enumerate(data):
            self.table.move(child, "", index)

        self.table.heading(column, command=lambda: self.sort_column(column, not reverse))

    def setBackround(self, frame:tk.Frame, image:str, width:int, height:int):
        #Sets up the backroound
        image = Image.open(image)
        img_w, img_h = image.size
        image = image.resize((width, height))
        self.bg = ImageTk.PhotoImage(image)
        self.backround = tk.Canvas(frame, highlightthickness=0, relief="ridge", border=0)
        self.backround.create_image(0, 0, image=self.bg, anchor="nw")
        self.backround.pack(fill="both", expand=True)
    
    def refresh_table(self):
        for book in self.table.get_children():
            self.table.delete(book)
        
        self.tableFill()

    def loan_book(self):
        try:
            selected_bookID = self.table.selection()[0]
            selected_book = self.table.item(selected_bookID, "values")#Tuple of the books selected
        except IndexError:
            self.errorLabel.config(text="Please select a book to loan out")
            return
        
        book = Book(*selected_book)
        
        found_book = self.library.get_book(book.isbn, "", "")

        if found_book == None:
            self.errorLabel.config(text="")
            self.errorLabel.config(text="Please select a book to loan out")
            return
        
        if book.stock > 0:
            loaned_book = self.user.loan_out(book)

            if loaned_book == None:
                self.errorLabel.config(text="You already have the book loaned out")
                return

            book.stock -= 1
            self.library.updateInfo(book.isbn, book.title, book.author, book.section, book.stock)
            self.errorLabel.config(text="")
            self.errorLabel.config(text=f"You loaned out {book.title} by {book.author}. Enjoy it!!")
        else:
            self.errorLabel.config(text="")
            self.errorLabel.config(text=f"We are sorry but, {book.title} by {book.author} is out of stock.")     

if __name__ == "__main__":
    root = tk.Tk()
    app = BrowseLibrary(root, "user")
    root.mainloop()

