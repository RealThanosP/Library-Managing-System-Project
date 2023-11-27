import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class EditBookPopApp:
    
    add_placeholder = ("Isbn:", "Title:", "Author:", "Section:", "Stock:")
    
    def __init__(self, root):
        self.editBookEntries = []
        self.root = root
        self.root.title("Edit Book Info")
        self.root.geometry("270x300")
        self.root.attributes('-topmost', 'true')

        #Main frame:
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        #Title Label
        self.titleLabel = tk.Label(self.frame, 
                                text="Edit Book", 
                                justify="center",
                                font=("Helvetica",20))
        self.titleLabel.grid(row=0, column=0, columnspan=2)
        
    #Entries for the book data inputs
        for i in range(5):
        #Creates 5 input fielsds to fill:
            self.editBookField = tk.Entry(self.frame, borderwidth=5, width=25)
            self.editBookField.grid(row=i+1, column=1, sticky="w")
        #Adds all the entries to a list to be used later to extract the data:
            self.editBookEntries.append(self.editBookField)
        #Create the pointing labels to the entries:
            self.editBookLabel = tk.Label(self.frame, text=self.add_placeholder[i], justify="right")
            self.editBookLabel.grid(row=i+1, column=0, sticky="we")

    #Find Button
        self.findButton = tk.Button(self.frame, text="Find", 
                                    pady=15, padx=15,
                                    font=("Helvetica", 18),
                                    command=self.editBook)
        self.findButton.grid(row=6,column=0)

    #Submit Button
        self.submitButton = tk.Button(self.frame, text="Submit", 
                                    pady=15, padx=15,
                                    font=("Helvetica", 18),
                                    command=self.submitChanges)
        self.submitButton.grid(row=6,column=1)

    #Error-Label
        self.errorLabel = tk.Label(self.frame, text="")
        self.errorLabel.grid(row=7, column=0, columnspan=2)

    def findBook(self):
        '''Main search function. Returns tuple: (isFound, string of the book found)'''
        #Gets the inputs form the entries
        isbn = self.editBookEntries[0].get()
        title = self.editBookEntries[1].get()
        author = self.editBookEntries[2].get()
        section = self.editBookEntries[3].get()
        stock = self.editBookEntries[4].get()
        #Opens the file to search for matching isbn or (title and author)
        with open("database.txt", "r", encoding="utf-8") as database:
            found = False
            book = ""
            for book in database:
                book = book.strip("\n").split("\t")
                #Checks if the Isbn entry input is already in the database.txt
                try:
                    if isbn == book[0] or (title == book[1] and author == book[2]):
                        found = True
                    if found: break
                except IndexError: 
                    self.errorLabel.config(text="There is no book in the database")
        return found, book

    def editBook(self):

        def updateEntries(book):
            #Deletes whatever you wrote
            for i, v in enumerate(self.editBookEntries):
                self.editBookEntries[i].delete(0, "end")

            #Prints the info from database on the entries
            for entryIndex, attribute in enumerate(book):
                self.editBookEntries[entryIndex].insert(0, attribute)

        #If the book is found then it just updates the Entries to the current book data
        if self.findBook()[0]:
            bookInfoList = self.findBook()[1]
            updateEntries(bookInfoList)
        else:
            for i in range(len(self.editBookEntries) - 1): self.editBookEntries[i].delete(0, "end")
            self.errorLabel.config(text="This book isn't in the library's database")
  
    
    def submitChanges(self):
        book = ""
        for index, content in enumerate(self.editBookEntries):
            book += f"{self.editBookEntries[index].get()}\t"
        
        print(book)
        with open("database.txt", "r", encoding="utf-8") as fileR:
            lines = fileR.readlines()

        with open("database.txt", "w", encoding="utf-8") as fileW:
            for line in lines:
                if line != book:
                    fileW.write(book)
                else:
                    fileW.write(line)

class AddBookPopApp:
    add_placeholder = ("Isbn:", "Title:", "Author:", "Section:", "Stock:")

    def __init__(self, root):
        self.addBookEntries = []
        self.root = root
        self.root.title("Add Book")
        self.root.geometry("270x300")
        self.root.attributes('-topmost', 'true')

    #Main frame:
        self.frame = tk.Frame(root)
        self.frame.pack()

    #Title Label 
        self.topLabel = tk.Label(self.frame, 
                                text="Add Book", 
                                justify="center",
                                font=("Helvetica",20))
        self.topLabel.grid(row=0, column=0, columnspan=2)

    #Entries for the book data inputs
        for i in range(5):
        #Creates 5 input fielsds to fill:
            self.addBookField = tk.Entry(self.frame, borderwidth=5, width=25)
            self.addBookField.grid(row=i+1, column=1, sticky="w")
        #Adds all the entries to a list to be used later to extract the data:
            self.addBookEntries.append(self.addBookField)
        #Create the pointing labels to the entries:
            self.addBookLabel = tk.Label(self.frame, text=self.add_placeholder[i], justify="right")
            self.addBookLabel.grid(row=i+1, column=0, sticky="we")

    #Add Button
        self.addButton = tk.Button(self.frame, 
                                    text="Submit", 
                                    pady=15, padx=15,
                                    font=("Helvetica", 18),
                                    command=self.addBook)
        self.addButton.grid(row=6,column=1, columnspan=3)

    #Error Label at the bottom 
        self.errorLabel = tk.Label(self.frame, text="")
        self.errorLabel.grid(row=7, column=0, columnspan=3)
    
    
    #Function for the SUMBIT button
    def addBook(self):
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
        #Just makes sure isbn and the remaining items are integers:
        except ValueError:
            self.errorLabel.config(text="The data you entered are invalid\n Try again: ")
            
        try:
            #List of attributes of the book
            atributes = [str(isbn), title, author, str(section),str(stock)]
            book = "\n" + "\t".join(atributes)
            #Takes the inputs to a list and then passes them into database.txt:
            #Passes the data to the databases part:
            database = open("database.txt", "a", encoding="utf-8")
            database.write(book)
            database.close()
            messagebox.showinfo(title="A Message", message="Book Added ✔")
        except UnboundLocalError:
            self.errorLabel.config(text="Fill all the required fields")
        
class App:
    editBookEntries = []
    loanBookEntries = []

    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("700x600")
    #Defines the main-frame and packs it into the screen:
        self.frame = tk.Frame(root)
        self.frame.pack()

    #Search-bar-section:
    #Search-bar:
        self.searchBar = tk.Entry(self.frame, borderwidth=5, width = 90)
        self.searchBar.grid(row=0, column=0, columnspan=5)

    #Search-button:
        self.searchButton = tk.Button(self.frame, text="Search")
        self.searchButton.grid(row=0, column=5)

    #Adding/Edit-book-section:
    #Edit Book-button
        self.editBook = tk.Button(self.frame, text="Edit Book", command=self.editBookDetails, width=10, height=2)
        self.editBook.grid(row=1, column=0, pady=20)
    #Add Book-button
        self.addBook = tk.Button(self.frame, text="Add Book", command=self.addNewBook, width=10, height=2)
        self.addBook.grid(row=2, column=0, pady=20)

    #Error-text-label:
        self.errorLabel = tk.Label(self.frame)
        self.errorLabel.grid(row=7,column=0, columnspan=2)
    #Loaning-book-section:
    #Loan-book-button
        self.loanButton = tk.Button(self.frame, text="Loan", width=10, height=2)
        self.loanButton.grid(row=1, column=2,columnspan=2)
            
    #Return-book-section:
    #Return-button:
        self.returnButton = tk.Button(self.frame, text="Return", width=10, height=2)
        self.returnButton.grid(row=1, column=4)

    #kill button (for develiping purposes only)
        self.kill = tk.Button(self.frame, text="KILL", font=("Ariel", 20), command=self.kill)
        self.kill.grid(row=10, column=0, columnspan=10)

    def kill(self):
        self.root.destroy()

    def editBookDetails(self):
        '''Opens a new Window that's for a editing book attributes'''
        masterEdit = tk.Toplevel(self.root)
        newWindow = EditBookPopApp(masterEdit)
        masterEdit.mainloop()

    def addNewBook(self):
        '''Opens a new window, that's just for adding new books to database.txt and handles all the desired changes of the selected title'''
        masterAdd = tk.Toplevel(self.root)
        newWindow = AddBookPopApp(masterAdd)
        masterAdd.mainloop()
        
    def search(self):
        '''Search button function'''
        return

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()





        