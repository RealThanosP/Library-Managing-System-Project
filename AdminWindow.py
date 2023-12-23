import tkinter as tk
from tkinter import ttk, messagebox
from database import Database, Book
from PIL import Image,ImageTk

class AdminPopUp:
    def __init__(self, root, username):
        self.name = username
        self.root = root
        self.root.minsize(1000,700)
        self.root.geometry("850x700")
        self.root.title(f"Our Library")
        
        #Initialize the library
        self.library = Database("Library.db")
        
        #Top frame:
        self.frameTop = tk.Frame(self.root, bg="#D2B48C")
        self.frameTop.pack(fill="both")

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

        #Frame for the table tree
        self.frameTable = tk.Frame(self.frameTop, bg="#D2B48C")
        self.frameTable.pack()

        #Table scrollbar:
        self.tableScroll = tk.Scrollbar(self.frameTable)
        self.tableScroll.pack(side="right", fill="y", pady=20)
        

        self.table = ttk.Treeview(self.frameTable, yscrollcommand=self.tableScroll.set)
        self.tableScroll.configure(command=self.table.yview)
        self.table.bind("<<TreeviewSelect>>", self.table_on_select)
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

        self.refreshButton = tk.Button(self.frameTop, text="⟳", command= self.refresh_table)
        self.refreshButton.pack()
        
        #Secondary frame to handle the buttons and the user interface
        #of the changest to the table and the database
        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack(expand = True, fill="both")

        #Places the backround of the window
        self.setBackround(self.frame, "background.png", 1920, 1080)
       

        #Add book section
        self.addSection(self.frame)
        self.frameAdd.place(relx=0.2, rely=0.05, anchor="n")

        #Edit a book's details section
        self.editSection(self.frame)
        self.frameEdit.place(relx=0.5, rely=0.05, anchor="n")
    
    def setBackround(self, frame, image, width, height):
        #Sets up the backroound
        image = Image.open(image)
        img_w, img_h = image.size
        image = image.resize((width, height))
        self.bg = ImageTk.PhotoImage(image)
        self.backround = tk.Canvas(frame, highlightthickness=0, relief="ridge", border=0)
        self.backround.create_image(0, 0, image=self.bg, anchor="nw")
        self.backround.pack(fill="both", expand=True)

    def findBook(self):
        '''Main search function. Returns tuple: (isFound, string of the book found)'''
        isFound = False
        #Gets the inputs form the entries
        isbn = self.editBookEntries[0].get()
        title = self.editBookEntries[1].get()
        author = self.editBookEntries[2].get()
        error = ""#Controls the text shown to the user based on if book is found
        
        library = Database("Library.db")
        book = library.get_book(isbn, title, author)
        
        if book: isFound = True

        return isFound, book

    def table_on_select(self, event):
        try:
            selectedBook = self.table.selection()[0]  # Get the ID of the selected book
            bookValues = self.table.item(selectedBook, "values") #Extracts it's value
        except Exception as error:
            print(str(error))
            return

        try:
            for index, entry in enumerate(self.editBookEntries):
                entry.delete(0,"end")
                entry.insert(0, bookValues[index])
        except Exception as error:
            for index, entry in enumerate(self.editBookEntries):
                entry.delete(0,"end")

    def tableFill(self):
        book_list = self.library.show_database()

        for book in book_list:
            #Inserts the values
            self.table.insert("", "end", value=book)

    def addSection(self, frame):
        #Main frame:
        self.BookAttributes = ("Isbn:", "Title:", "Author:", "Section:", "Stock:")
        self.addBookEntries = []
        self.frameAdd = tk.Frame(frame, bg="#D2B48C")

        #Entry Frame:
        self.frameOfEntries = tk.Frame(self.frameAdd, bg="#D2B48C")

        #Label frame:
        self.frameOfLabels = tk.Frame(self.frameAdd, bg="#D2B48C")

        #Title Label 
        self.topLabel = tk.Label(self.frameAdd, 
                                text="Add a Book", 
                                justify="center",
                                bg="#D2B48C",
                                font=("Helvetica",20))

        #Entries for the book data inputs
        for i in range(5):
        #Creates 5 input fielsds to fill:
            self.addBookField = tk.Entry(self.frameOfEntries, borderwidth=5, width=25)
            self.addBookField.pack(pady=4)
        #Adds all the entries to a list to be used later to extract the data:
            self.addBookEntries.append(self.addBookField)
        #Create the pointing labels to the entries:
            self.addBookLabel = tk.Label(self.frameOfLabels, text=self.BookAttributes[i], bg="#D2B48C")
            self.addBookLabel.pack(pady=7)

        #Add Button
        self.addButton = tk.Button(self.frameAdd, 
                                    text="Submit", 
                                    pady=15, padx=15,
                                    font=("Helvetica", 20),
                                    bg="#CFCFCF",
                                    command=self.addBook)

        #Error Label at the bottom 
        self.errorLabelAdd = tk.Label(self.frameAdd, text="", bg="#D2B48C", justify="center")

        #Places evry frame on the screen:
        self.topLabel.grid(row=0, column=1, columnspan=2, padx=(0,70), pady=10)
        self.frameOfLabels.grid(row=1, column=0)
        self.frameOfEntries.grid(row=1, column=1)
        self.addButton.grid(row=2, column=0, columnspan=2, pady=(20,0))
        self.errorLabelAdd.grid(row=3, column=0, columnspan=3, pady=(10,0))

    def addBook(self):
        '''Function for the SUMBIT button'''
        book_data = ""
        #The for-loop that Gives access to the entries separetely
        for i in range(5):
            book_data += self.addBookEntries[i].get() + "\n"
            self.addBookEntries[i].delete(0,"end")
        
        book_data = book_data.split("\n")

        try:
            #Checks the input's correctness:
            isbn = int(book_data[0])
            title = book_data[1]
            author = book_data[2]
            section = int(book_data[3])
            stock = int(book_data[4])

            #Commits the changes to the database
            database = Database("Library.db")
            check = database.add_book_database(isbn, title, author, section, stock)

            #Let the user know the status of the bookAdding process
            if check == "This book is already in the database.\nYou can edit it's details on the other window.":
                self.errorLabelAdd.config(text=check)
            elif check == 'Book successfully added!':
                messagebox.showinfo(title="Adding Books", message="Book Added ✔")
                self.errorLabelAdd.config(text="")
            else:
                self.errorLabelAdd.config(text=check)

        #Just makes sure isbn and the remaining items are integers:
        except ValueError:
            self.errorLabelAdd.config(text="The data you entered are invalid, Try again: ")
            
    def editSection(self, frame):
        self.editBookEntries = []

        #Main frame:
        self.frameEdit = tk.Frame(frame, bg="#D2B48C")

        #Title fame:
        self.frameEditTitle = tk.Frame(self.frameEdit,bg="#D2B48C")

        #Entry frame:
        self.frameEditEntries = tk.Frame(self.frameEdit,bg="#D2B48C")

        #Entries label frame
        self.frameEditLabels = tk.Frame(self.frameEdit,bg="#D2B48C")

        #Buttons frame:
        self.frameEditButtons = tk.Frame(self.frameEdit,bg="#D2B48C")

        #Error Label Frame
        self.frameEditError = tk.Frame(self.frameEdit,bg="#D2B48C")

        #Title Label
        self.titleLabel = tk.Label(self.frameEditTitle, 
                                text="Edit a Book", 
                                justify="center",
                                font=("Helvetica",20),
                                bg="#D2B48C"
                                )
        self.titleLabel.pack(pady=10, padx=60)
        
        #Entries for the book data inputs
        for i in range(5):
        #Creates 5 input fielsds to fill:
            self.editBookField = tk.Entry(self.frameEditEntries, borderwidth=5, width=25)
            self.editBookField.pack(pady=4)
        #Adds all the entries to a list to be used later to extract the data:
            self.editBookEntries.append(self.editBookField)
        #Create the pointing labels to the entries:
            self.editBookLabel = tk.Label(self.frameEditLabels, text=self.BookAttributes[i], justify="center", bg="#D2B48C")
            self.editBookLabel.pack(pady=7)

        #Submit Button
        self.submitButton = tk.Button(self.frameEditButtons, text="Submit", 
                                    pady=15, padx=15,
                                    font=("Helvetica", 20),
                                    bg="#CFCFCF",
                                    command=self.submitChanges)
        self.submitButton.pack(side="left")

        #Submit Button
        self.clearButton = tk.Button(self.frameEditButtons, text="Clear", 
                                    pady=15, padx=15,
                                    font=("Helvetica", 20),
                                    bg="#CFCFCF",
                                    command=lambda: self.clear_text(self.editBookEntries))
        self.clearButton.pack(side="right")

        #Error-Label
        self.errorLabelEdit = tk.Label(self.frameEditError, text="", bg="#D2B48C")
        self.errorLabelEdit.pack()

        #Places all the frame in the screen:
        self.frameEditTitle.grid(row=0, column=0, columnspan=2)
        self.frameEditLabels.grid(row=1, column=0)
        self.frameEditEntries.grid(row=1, column=1)
        self.frameEditButtons.grid(row=2,column=0,columnspan=2, pady=(20,0))
        self.frameEditError.grid(row=3,column=0,columnspan=2, pady=(10,0))
    
    def editBook(self):

        def updateEntries(book):
            #Deletes whatever you wrote
            for i, entry in enumerate(self.editBookEntries):
                entry.delete(0, "end")

            #Prints the info from database on the entries
            for entryIndex, attribute in enumerate(book):
                self.editBookEntries[entryIndex].insert(0, attribute)

        #If the book is found then it just updates the Entries to the current book data
        if self.findBook()[0]:
            bookInfoList = self.findBook()[1]#tuple
            updateEntries(bookInfoList)
        else:#If not found just deletes the info
            for i, entry in enumerate(self.editBookEntries): 
                entry.delete(0, "end")
            self.errorLabelEdit.config(text="The book was not found")

    def submitChanges(self):
        """To be changed with the addition of the SQLite database"""
        #Gets the inputs form the entries
        isbn = self.editBookEntries[0].get()
        title = self.editBookEntries[1].get()
        author = self.editBookEntries[2].get()
        section = self.editBookEntries[3].get()
        stock = self.editBookEntries[4].get()

        if not (isbn and title and author and section and stock):
            self.errorLabelEdit.config(text="Please fill out all the inputs")
            return None 
        #Deletes whatever you wrote
        for i, entry in enumerate(self.editBookEntries):
            entry.delete(0, "end")
        
        #Commits the changes into the database
        library = Database("Library.db")
        error = library.updateInfo(isbn, title, author, section, stock)
        self.errorLabelEdit.config(text=error)
        self.tableFill()

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
    
    def clear_text(self, entryList):
        '''Clears all the text from any set of entries you insert'''
        for entry in entryList:
            entry.delete(0,"end")

        if entryList == self.editBookEntries:
            self.errorLabelEdit.config(text="Text successfully cleared")

    def refresh_table(self):
        # Clear existing treeview content
        for item in self.table.get_children():
            self.table.delete(item)
        # Repopulate treeview with updated data
        self.tableFill()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminPopUp(root, "admin")
    root.mainloop()