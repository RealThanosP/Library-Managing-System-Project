import tkinter as tk
from tkinter import ttk

class AddBookPopApp:
    editBookEntries = []
    add_placeholder = ("Isbn:", "Title:", "Author:", "Stock:")

    def __init__(self, root):
        self.root = root
        self.root.title("Add Book")
        self.root.geometry("270x300")

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
        for i in range(4):
        #Creates 5 input fielsds to fill:
            self.editBookField = tk.Entry(self.frame, borderwidth=5, width=25)
            self.editBookField.grid(row=i+1, column=1, sticky="w")
        #Adds all the entries to a list to be used later to extract the data:
            self.editBookEntries.append(self.editBookField)
        #Create the pointing labels to the entries:
            self.editBookLabel = tk.Label(self.frame, text=self.add_placeholder[i], justify="right")
            self.editBookLabel.grid(row=i+1, column=0, sticky="we")

    #Add Button
        self.addButton = tk.Button(self.frame, 
                                    text="Submit", 
                                    pady=15, padx=15,
                                    font=("Helvetica", 18),
                                    command=self.addBook)
        self.addButton.grid(row=5,column=1, columnspan=3)

    #Error Label at the bottom 
        self.errorLabel = tk.Label(self.frame, text="")
        self.errorLabel.grid(row=6, column=0, columnspan=3)
    
    #Function for the SUMBIT button
    def addBook(self):
        book_data = ""
        #The for-loop that Gives access to the entries separetely
        for i in range(4):
            book_data += self.editBookEntries[i].get() + "\n"
            self.editBookEntries[i].delete(0,"end")
        
        book_data = book_data.split("\n")

        try:
            #Checks the input's correctness:
            isbn = int(book_data[0])
            title = book_data[1]
            author = book_data[2]
            stock = int(book_data[3])
        #Just makes sure isbn and the remaining items are integers:
        except ValueError:
            self.errorLabel.config(text="The data you entered are invalid\n Try again: ")
        
        #Takes the inputs to a list and then passes them into database.txt:
        #Passes the data to the databases part:
            #List of attributes of the book
        try:
            atributes = [str(isbn), title, author, str(stock)]
            book = "\t".join(atributes) + "\n"
            database = open("database.txt", "a", encoding="utf-8")
            database.write(book)
            database.close()
            self.errorLabel.config(text="Book Added ✔️")
        except UnboundLocalError:
            self.errorLabel.config(text="Fill all the required fields")

class App:
    editBookEntries = []
    loanBookEntries = []

    edit_placeholder = ("Isbn:", "Title:", "Author:", "Summary:", "Stock:")
    loan_placeholder = ("Find by Isbn:", "Find by Title:")
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

    #Adding-book-section:
    #Add-a-book-button
        self.editBook = tk.Button(self.frame, text="Edit Book", command=self.editBookDetails)
        self.editBook.grid(row=1, column=0, columnspan=2)
    #Error-text-label:
        self.errorLabel = tk.Label(self.frame)
        self.errorLabel.grid(row=7,column=0, columnspan=2)
    #The inputs for the atributes of the new book:
        for i in range(0,5):
        #Creates 5 input fielsds to fill:
            self.editBookField = tk.Entry(self.frame, borderwidth=5, width=25)
            self.editBookField.grid(row=i+2, column=1, sticky="w")
        #Adds all the entries to a list to be used later to extract the data:
            self.editBookEntries.append(self.editBookField)
        #Create the pointing labels to the entries:
            self.editBookLabel = tk.Label(self.frame, text=self.edit_placeholder[i], justify="right")
            self.editBookLabel.grid(row=i+2, column=0, sticky="we")

    #Loaning-book-section:
    #Loan-book-button
        self.loanButton = tk.Button(self.frame, text="Loan")
        self.loanButton.grid(row=1, column=2,columnspan=2)
        #Loan-labels:
        for i in range(2,4):
            self.loanLabel = tk.Label(self.frame, text=self.loan_placeholder[i-2])
            self.loanLabel.grid(row=i, column=2, sticky="we")
    
    #Loan-book-field:
        for i in range(2,4):
            self.loanBookField = tk.Entry(self.frame, borderwidth=5, width=25)
            self.loanBookField.grid(row=i,column=3,sticky="w")
            self.loanBookEntries.append(self.loanBookField)
            
    #Return-book-section:
    #Return-button:
        self.returnButton = tk.Button(self.frame, text="Return")
        self.returnButton.grid(row=1, column=4)

    #kill button (for develiping purposes only)
        self.kill = tk.Button(self.frame, text="KILL", font=("Ariel", 20), command=self.kill)
        self.kill.grid(row=10, column=0, columnspan=10)

    def kill(self):
        self.root.destroy()

    def editBookDetails(self):
        '''Opens a new window, that's just for adding new books to database.txt, when 'Add Book' button is pressed and isbn is not in database
        and handles all the desired changes of the selected title'''
        with open("database.txt", "r", encoding="utf-8") as database:
            found = False
            for book in database:
                book = book.split("\t")
                #Checks if the Isbn entry input is already in the database.txt
                if self.editBookEntries[0].get() == book[0]:
                    found = True

                if found: break#Prematurely terminates the for-loop to make the process kind of faster

                #Checks if the Isbn entry input is empty
                if not self.editBookEntries[0].get():
                    found = True
                    self.errorLabel.config(text="Fill all the required fields")
                    break
        if not found:
            master = tk.Toplevel(self.root)
            newWindow = AddBookPopApp(master)
            master.mainloop()
        
    def search(self):
        '''Search button function'''
        return

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
