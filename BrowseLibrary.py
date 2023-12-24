import tkinter as tk
from tkinter import ttk
from database import Database, Book
from PIL import Image, ImageTk
from User import User
import os

class BrowseLibrary:
    def __init__(self, root, username):
        self.name = username
        self.root = root
        self.root.title("Browse the library")
        self.root.geometry("1000x700")
        self.root.minsize(1400, 700)
        self.root.maxsize(1800, 900)
        #Inittialize the library
        self.library = Database("Library.db")
        self.user = User(self.name)

        #Top Frame
        self.frameTop = tk.Frame(self.root, bg="#D2B48C")
        self.frameTop.pack(fill="both")

        #Places the table into the screen 
        self.tableSection(self.frameTop)

        #Bottom user main Frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True, fill="both")

        #Sets the background of the main frame:
        self.setBackround(self.frame, "background.png", 1900, 800)

        #Loan Button
        self.loanButton = tk.Button(self.frame,
                                    text="Loan Selected",
                                    font=("Helvetica", 20),
                                    padx=15, pady=15,
                                    border=0,
                                    bg="#C3C3C3",
                                    command=self.loan_book)
        self.loanButton.place(relx=0.15, rely=0.12, anchor="n")

        #Return Button
        self.returnButton = tk.Button(self.frame,
                                      text="Return Selected",
                                      font=("Helvetica", 20),
                                      padx=15,pady=15,
                                      border=0,
                                      bg="#C3C3C3",
                                      command=self.return_book)
        self.returnButton.place(relx=0.15, rely=0.3, anchor="n")

        #Table frame for the already owned books
        self.frameUser = tk.Frame(self.frame)
        self.frameUser.place(relx=0.35, rely=0.1, anchor="nw")

        self.tableUser = ttk.Treeview(self.frameUser)
        #Table scrollbar:
        self.tableUserScroll = tk.Scrollbar(self.frameUser)
        self.tableUserScroll.pack(side="right", fill="y")
        
        self.tableUser = ttk.Treeview(self.frameUser, yscrollcommand=self.tableUserScroll.set)
        self.tableUserScroll.configure(command=self.tableUser.yview)
        #Define the columns of the table:
        self.tableUser["columns"] = ("ISBN", "Title", "Author", "Section")
        
        #Format the columns:
        self.tableUser.column("#0", width=0, stretch="NO")
        self.tableUser.column("ISBN", width=100, minwidth=25)
        self.tableUser.column("Title", width=300, minwidth=125)
        self.tableUser.column("Author", width=120, minwidth=80)
        self.tableUser.column("Section", width=60, minwidth=60)

        #Create the headings
        self.tableUser.heading("#0", text="", anchor="w")
        self.tableUser.heading("ISBN", text="ISBN", anchor="w", command=lambda: self.sort_column("ISBN", False))
        self.tableUser.heading("Title", text="Title", anchor="center", command=lambda: self.sort_column("Title", False))
        self.tableUser.heading("Author", text="Author", anchor="center", command=lambda: self.sort_column("Author", False))
        self.tableUser.heading("Section", text="Section", anchor="w", command=lambda: self.sort_column("Section", False))
       
        
        #Fills up the table with database data
        self.tableUserFill()
        self.tableUser.pack()

        #Error label
        self.errorLabel = tk.Label(self.frame, text="", bg="#D2B48C")
        self.errorLabel.place(relx=0.5, rely=0.9, anchor="s")

    def tableSection(self, frame):
        # Table Frame
        self.frameTable = tk.Frame(frame, bg="#D2B48C")
        self.frameTable.pack()

        #Button to sign out
        self.backButton = tk.Button(frame, 
                                       text="↩Back to Main Menu", 
                                       font=("Helvetica", 15), 
                                       bg="#CFCFDF",
                                       command=self.openSignInWindow)
        self.backButton.place(relx=0.01, rely=0.05, anchor="w")

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

        #Refresh button:
        self.refreshButton = tk.Button(frame, 
                                       text="⟳", 
                                       bg="#C3C3C3",
                                       border=0,
                                       padx=10,pady=10,
                                       command=self.refresh_tables)
        self.refreshButton.pack()

    def tableFill(self):
        '''Fills up the table with the values from the database'''
        book_list = self.library.show_database()

        for book in book_list:
            self.table.insert("", "end", value=book)

    def tableUserFill(self):
        '''Fills up the table where the users can see his loaned out books'''
        #Checks for the book in the users file of loans
        def create_file_if_not_exist(folder_path, file_name):
            file_path = os.path.join(folder_path, file_name)
            if not os.path.exists(file_path):
                # Create the file if it doesn't exist
                with open(file_path, 'w'):
                    pass  # Empty context manager to create the file

        create_file_if_not_exist("UserFiles", f"{self.name}.txt")

        with open(f"UserFiles/{self.name}.txt", "r", encoding="utf-8") as file:
            for line in file:
                data = line.strip().split("\t")
                self.tableUser.insert("", "end", values=tuple(data))
                
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
    
    def refresh_tables(self):
        for book in self.table.get_children():
            self.table.delete(book)
        
        for book in self.tableUser.get_children():
            self.tableUser.delete(book)

        self.tableFill()
        self.tableUserFill()

    def loan_book(self):
        #Resets the text of the errro label
        self.errorLabel.config(text="")
        try:
            selected_bookID = self.table.selection()
        except Exception as error:
            self.errorLabel.config(text="Please select a book to loan out")
            print(str(error))
            return
        
        for index, selection in enumerate(selected_bookID):
            try: selected_book = self.table.item(selected_bookID[index], "values")   
            except Exception as error: print(str(error))
            book = Book(*selected_book)
            
            found_book = self.library.get_book(book.isbn, "", "")

            if found_book == None:
                self.errorLabel.config(text="")
                self.errorLabel.config(text="Please select a book to loan out")
                return
            
            if book.stock > 0:
                loaned_book = self.user.loan_out(book)

                if loaned_book == None:
                    self.errorLabel.config(text="You already have one of the selected book loaned out")
                    return

                book.stock -= 1
                self.library.updateInfo(book.isbn, book.title, book.author, book.section, book.stock)
                before_text = self.errorLabel.cget("text")
                self.errorLabel.config(text=f"{before_text}\nYou loaned out {book.title} by {book.author}. Enjoy it!!\n")
                self.refresh_tables()
            else:
                self.errorLabel.config(text=f"We are sorry but, {book.title} by {book.author} is out of stock.")     

    def return_book(self):
        '''Return the loaned out books to the library'''
        try:
            selectionID = self.tableUser.selection()
        except Exception as error:
            self.errorLabel.config(text="Plese select a book to return")
            print(str(error))
            return

        for index, selection in enumerate(selectionID):
            try: selected_book = self.tableUser.item(selectionID[index], "values")   
            except Exception as error: 
                print(str(error))
                return
            
            book = Book(*selected_book, 0)

            found_book = self.library.get_book(book.isbn, "", "")

            book = Book(*found_book)

            if found_book == None:
                self.errorLabel.config(text="Please select a book to return")
                return
            
            returned_book = self.user.return_in(book)

            book.stock += 1
            self.library.updateInfo(book.isbn, book.title, book.author, book.section, book.stock)
            self.errorLabel.config(text=f"You successfully returned {book.title} by {book.author}.\nThank you for the preference")
            self.refresh_tables()

    def openMainMenu(self):
        self.root.destroy()
        app = App(root, self.name)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = BrowseLibrary(root, "user")
    root.mainloop()

