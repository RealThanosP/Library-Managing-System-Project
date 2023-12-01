import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image

class App:
    BookAttributes = ("Isbn:", "Title:", "Author:", "Section:", "Stock:")

    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System") 
        self.root.geometry("900x500+900+100")
        self.root.wm_minsize(900, 500)

        #Defines the main-frame and packs it into the screen:
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)
        
        #Background Image
        self.backgroundImg = Image.open("background.png")
        self.backLabel = ImageTk.PhotoImage(self.backgroundImg)
        
        self.backLabel = tk.Label(self.frame, image=self.backLabel)
        self.backLabel.pack()

        #Places the frame of the add book section on the screen
        self.addSection(self.frame)
        self.frameAdd.place(x=20, rely=0.05)

        #Places the frame of the edit book section on the screen
        self.EditSection(self.frame)
        self.frameEdit.place(x=250, rely=0.05)
        
        #Place the frame of the loan a book section on the screen
        self.LoanSection(self.frame)
        self.frameLoan.place(x=530, rely=0.05)#69 NICE!!!

        #Kill Button (For developing reasons only)
        self.frameKill = tk.Frame(self.frame, bg="red")
        self.killButton = tk.Button(self.frameKill, text="KILL", font=("Helvetica", 20), width=10, height=3, command=self.kill)
        



    def kill(self):
        self.root.destroy()
    
    #Add Book Frame
    def addSection(self, frame):
        #Main frame:
        self.addBookEntries = []
        self.frameAdd = tk.Frame(frame)


        #Title Label 
        self.topLabel = tk.Label(self.frameAdd, 
                                text="Add a Book", 
                                justify="center",
                                font=("Helvetica",20))
        self.topLabel.grid(row=0, column=0, columnspan=2)

        #Entries for the book data inputs
        for i in range(5):
        #Creates 5 input fielsds to fill:
            self.addBookField = tk.Entry(self.frameAdd, borderwidth=5, width=25)
            self.addBookField.grid(row=i+1, column=1, sticky="w")
        #Adds all the entries to a list to be used later to extract the data:
            self.addBookEntries.append(self.addBookField)
        #Create the pointing labels to the entries:
            self.addBookLabel = tk.Label(self.frameAdd, text=self.BookAttributes[i], justify="center")
            self.addBookLabel.grid(row=i+1, column=0, sticky="we")

        #Add Button
        self.addButton = tk.Button(self.frameAdd, 
                                    text="Submit", 
                                    pady=15, padx=15,
                                    font=("Helvetica", 18),
                                    command=self.addBook)
        self.addButton.grid(row=6,column=1, columnspan=2, sticky="w")

        #Error Label at the bottom 
        self.errorLabelAdd = tk.Label(self.frameAdd, text="")
        self.errorLabelAdd.grid(row=7, column=0, columnspan=3)
    
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
        #Just makes sure isbn and the remaining items are integers:
        except ValueError:
            self.errorLabelAdd.config(text="The data you entered are invalid\n Try again: ")
            
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
            self.errorLabelAdd.config(text="Fill all the required fields")

    #Edit Book Frame
    def EditSection(self, frame):
        self.editBookEntries = []

        #Main frame:
        self.frameEdit = tk.Frame(frame)

        #Title Label
        self.titleLabel = tk.Label(self.frameEdit, 
                                text="Edit a Book", 
                                justify="center",
                                font=("Helvetica",20))
        self.titleLabel.grid(row=0, column=0, columnspan=2)
        
        #Entries for the book data inputs
        for i in range(5):
        #Creates 5 input fielsds to fill:
            self.editBookField = tk.Entry(self.frameEdit, borderwidth=5, width=25)
            self.editBookField.grid(row=i+1, column=1, sticky="w")
        #Adds all the entries to a list to be used later to extract the data:
            self.editBookEntries.append(self.editBookField)
        #Create the pointing labels to the entries:
            self.editBookLabel = tk.Label(self.frameEdit, text=self.BookAttributes[i], justify="center")
            self.editBookLabel.grid(row=i+1, column=0, sticky="we")

        #Find Button
        self.findButton = tk.Button(self.frameEdit, text="Find", 
                                    pady=15, padx=15,
                                    font=("Helvetica", 18),
                                    command=self.editBook)
        self.findButton.grid(row=6,column=0, sticky="e")

        #Submit Button
        self.submitButton = tk.Button(self.frameEdit, text="Submit\nChanges", 
                                    pady=1, padx=15,
                                    font=("Helvetica", 18),
                                    command=self.submitChanges)
        self.submitButton.grid(row=6,column=1)

        #Error-Label
        self.errorLabelEdit = tk.Label(self.frameEdit, text="")
        self.errorLabelEdit.grid(row=8, column=0, columnspan=2)
    
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
            bookInfoList = self.findBook()[1]
            updateEntries(bookInfoList)
        else:#If not found just deltes the info
            for i, entry in enumerate(self.editBookEntries): 
                entry.delete(0, "end")
            self.errorLabelEdit.config(text="This book isn't in the library's database")
  
    def submitChanges(self):
        """To be changed with the addition of the SQLite database"""
    
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

    #Loan Book Frame
    def LoanSection(self, frame):
        self.loanBookEntries = []
        #Defines the main frame
        self.frameLoan = tk.Frame(frame)
        
        #Title Label
        self.loanLabel = tk.Label(self.frameLoan, 
                                text="Loan a Book", 
                                justify="center",
                                font=("Helvetica",20))
        self.loanLabel.grid(row=0, column=0, columnspan=2)

        #Loan Book Entries for searching the book in the database based on [isbn OR (title AND author)]
        for i in range(3):
            #Entries
            self.loanEntry = tk.Entry(self.frameLoan, borderwidth=5, width=25)
            self.loanEntry.grid(row=i+1, column=1)
            #Entry list to manage their info seperately
            self.loanBookEntries.append(self.loanEntry)

            #The labels for the entries
            self.entryLabel = tk.Label(self.frameLoan, text=self.BookAttributes[i]) 
            self.entryLabel.grid(row=i+1, column=0)

        #The find Button
        self.loanFindButton = tk.Button(self.frameLoan, text="Find", 
                                        pady=15, padx=15,
                                        font=("Helvetica", 18),
                                        image="background.jpg",
                                        command=lambda: print(self.findBook))########### CHANGE THE FUNCTIOND
        self.loanFindButton.grid(row=4, column=0, pady=(52,0), padx=(15,0),sticky="e")

        #The Submit Button
        self.loanSubmitButton = tk.Button(self.frameLoan, text="Submit\nLoan", 
                                    pady=1, padx=15,
                                    font=("Helvetica", 18),
                                    bg="red",
                                    command=lambda: print(self.findbook))############# CHANGE THE FUNCTIONS
        self.loanSubmitButton.grid(row=4, column=1, pady=(52,0), padx=15)

        #Error Label
        self.errorLabelLoan = tk.Label(self.frameLoan, text="")
        self.errorLabelLoan.grid(row=5, column=0, columnspan=2, pady=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()





        