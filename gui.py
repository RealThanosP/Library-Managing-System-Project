import tkinter as tk
from tkinter import messagebox
from SignUp import SignUpPopUpApp
from User import User

class App:
    '''Opens the library App and handles all of it's functionalities'''
    BookAttributes = ("Isbn:", "Title:", "Author:", "Section:", "Stock:")

    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System") 
        self.root.geometry("1100x500-1700+100")
        self.root.resizable(False,False)

        #Defines the main-frame and packs it into the screen:
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        #Places the frame of the add book section on the screen
        self.addSection(self.frame)
        self.frameAdd.place(relx=0.02, rely=0.05)

        #Places the frame of the edit book section on the screen
        self.EditSection(self.frame)
        self.frameEdit.place(relx=0.3, rely=0.05)
        
        #Place the frame of the loan a book section on the screen
        self.LoanSection(self.frame)
        self.frameLoan.place(relx=0.58, rely=0.05)#69 NICE!!!

        #Kill Button (For developing reasons only)
        self.frameKill = tk.Frame(self.frame, bg="red")
        self.killButton = tk.Button(self.frameKill, text="KILL", font=("Helvetica", 20), width=10, height=3, command=self.kill)
        self.killButton.pack()
        self.frameKill.place(relx=0.5,rely=0.9, anchor="center")
        
    def kill(self):
        self.root.destroy()
    
    #Add Book Frame
    def addSection(self, frame):
        #Main frame:
        self.addBookEntries = []
        self.frameAdd = tk.Frame(frame)

        #Entry Frame:
        self.frameOfEntries = tk.Frame(self.frameAdd)

        #Label frame:
        self.frameOfLabels = tk.Frame(self.frameAdd)

        #Title Label 
        self.topLabel = tk.Label(self.frameAdd, 
                                text="Add a Book", 
                                justify="center",
                                font=("Helvetica",20))

        #Entries for the book data inputs
        for i in range(5):
        #Creates 5 input fielsds to fill:
            self.addBookField = tk.Entry(self.frameOfEntries, borderwidth=5, width=25)
            self.addBookField.pack()
        #Adds all the entries to a list to be used later to extract the data:
            self.addBookEntries.append(self.addBookField)
        #Create the pointing labels to the entries:
            self.addBookLabel = tk.Label(self.frameOfLabels, text=self.BookAttributes[i], justify="center")
            self.addBookLabel.pack(pady=6)

        #Add Button
        self.addButton = tk.Button(self.frameAdd, 
                                    text="Submit", 
                                    pady=15, padx=15,
                                    font=("Helvetica", 18),
                                    command=self.addBook)

        #Error Label at the bottom 
        self.errorLabelAdd = tk.Label(self.frameAdd, text="")

        #Places evry frame on the screen:
        self.topLabel.grid(row=0, column=1, columnspan=2, padx=(0,50))
        self.frameOfLabels.grid(row=1, column=0)
        self.frameOfEntries.grid(row=1, column=1)
        self.addButton.grid(row=2, column=0, columnspan=2)
        self.errorLabelAdd.grid(row=3, column=0, columnspan=2)

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

        #Title fame:
        self.frameEditTitle = tk.Frame(self.frameEdit)

        #Entry frame:
        self.frameEditEntries = tk.Frame(self.frameEdit)

        #Entries label frame
        self.frameEditLabels = tk.Frame(self.frameEdit)

        #Buttons frame:
        self.frameEditButtons = tk.Frame(self.frameEdit)

        #Error Label Frame
        self.frameEditError = tk.Frame(self.frameEdit)

        #Title Label
        self.titleLabel = tk.Label(self.frameEditTitle, 
                                text="Edit a Book", 
                                justify="center",
                                font=("Helvetica",20))
        self.titleLabel.pack()
        
        #Entries for the book data inputs
        for i in range(5):
        #Creates 5 input fielsds to fill:
            self.editBookField = tk.Entry(self.frameEditEntries, borderwidth=5, width=25)
            self.editBookField.pack()
        #Adds all the entries to a list to be used later to extract the data:
            self.editBookEntries.append(self.editBookField)
        #Create the pointing labels to the entries:
            self.editBookLabel = tk.Label(self.frameEditLabels, text=self.BookAttributes[i], justify="center")
            self.editBookLabel.pack(pady=6)

        #Find Button
        self.findButton = tk.Button(self.frameEditButtons, text="Find", 
                                    pady=15, padx=15,
                                    font=("Helvetica", 18),
                                    command=self.editBook)
        self.findButton.pack(side="left")

        #Submit Button
        self.submitButton = tk.Button(self.frameEditButtons, text="Submit\nChanges", 
                                    pady=2, padx=15,
                                    font=("Helvetica", 20),
                                    command=self.submitChanges)
        self.submitButton.pack(side="right")

        #Error-Label
        self.errorLabelEdit = tk.Label(self.frameEditError, text="")
        self.errorLabelEdit.pack()

        #Places all the frame in the screen:
        self.frameEditTitle.grid(row=0, column=0, columnspan=2)
        self.frameEditLabels.grid(row=1, column=0, sticky="e")
        self.frameEditEntries.grid(row=1, column=1)
        self.frameEditButtons.grid(row=2,column=0,columnspan=2)
        self.frameEditError.grid(row=3,column=0,columnspan=2)
    
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
        
        #Frame for the title:
        self.frameLoanTitle = tk.Frame(self.frameLoan)

        #Frame for the entries:
        self.frameLoanEntries = tk.Frame(self.frameLoan)

        #Frame for the labels:
        self.frameLoanLabels = tk.Frame(self.frameLoan)

        #Frame for the buttons
        self.frameLoanButtons = tk.Frame(self.frameLoan)

        #Frame for the error label
        self.frameLoanErrors = tk.Frame(self.frameLoan)
        
        #Title Label
        self.loanLabel = tk.Label(self.frameLoanTitle, 
                                text="Loan a Book", 
                                justify="center",
                                font=("Helvetica",20))
        self.loanLabel.pack()

        #Loan Book Entries for searching the book in the database based on [isbn OR (title AND author)]
        for i in range(3):
            #Entries
            self.loanEntry = tk.Entry(self.frameLoanEntries, borderwidth=5, width=25)
            self.loanEntry.pack()

            #Entry list to manage their info seperately
            self.loanBookEntries.append(self.loanEntry)

            #The labels for the entries
            self.entryLabel = tk.Label(self.frameLoanLabels, text=self.BookAttributes[i]) 
            self.entryLabel.pack(pady=7)

        #The find Button
        self.loanFindButton = tk.Button(self.frameLoanButtons, text="Find", 
                                        pady=15, padx=15,
                                        font=("Helvetica", 18),
                                        command=lambda: print(self.findBook))########### CHANGE THE FUNCTION
        self.loanFindButton.pack(side="left")

        #The Submit Button
        self.loanSubmitButton = tk.Button(self.frameLoanButtons, text="Submit\nLoan", 
                                    pady=2, padx=15,
                                    font=("Helvetica", 20),
                                    bg="red",
                                    command=lambda: print(self.findbook))############# CHANGE THE FUNCTIONS
        self.loanSubmitButton.pack(side="right")

        #Error Label
        self.errorLabelLoan = tk.Label(self.frameLoanErrors, text="OOps Erro")
        self.errorLabelLoan.grid(row=5, column=0, columnspan=2, pady=1)

        #Places all the frames into the screen
        self.frameLoanTitle.grid(row=0,column=0,columnspan=2)
        self.frameLoanLabels.grid(row=1, column=0)
        self.frameLoanEntries.grid(row=1,column=1)
        self.frameLoanButtons.grid(row=2,column=0,columnspan=2)
        self.frameLoanErrors.grid(row=3,column=0,columnspan=2)

class SignInPopUpApp:
        
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x400-1700+200")
        self.root.title("Library Management System")
        self.root.resizable(False, False)

        #Main Frame:
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand= True)

        #Places the Sign in section to the screen
        self.signInSection(self.frame)
        self.frameSignIn.pack()

        #Error Label
        self.errorLabel = tk.Label(self.frame)
        self.errorLabel.pack()

        #Frame for the bottom text
        self.signUpSection(self.frame)
        self.frameSignUp.place(relx=0.5, rely=0.9, anchor="center")



        #Kill Button
        self.frameKill = tk.Frame(self.frame)
        self.killButton = tk.Button(self.frameKill, text="KILL", font=("Helvetica", 20),command=self.kill)
        self.killButton.pack()
        self.frameKill.place(relx=0.2, rely=0.1, anchor="s")

    #Sign in section:
    def signInSection(self, frame):
        '''Handles the visible part where you can sign in to the platform'''
        #Main frame
        self.frameSignIn = tk.Frame(frame)

        #Frame for the entries
        self.frameEntries = tk.Frame(self.frameSignIn)

        #Frame for the buttons
        self.frameButtons = tk.Frame(self.frameSignIn)

        #Frame fo the title label:
        self.frameTitle = tk.Frame(self.frameSignIn)

        #Title Label:
        self.titleLabel = tk.Label(self.frameTitle, text="Join the App!!!", font=("Helvetica", 20))
        self.titleLabel.pack(pady=(20,60))

        #Functions to handle the changes of the temporary text in the entries
        def focusIn(entry, isUser):#When entry is clicked in
            entry.delete(0, "end")
            if isUser: entry.config(fg="white")
            else: entry.config(fg="white", show="*")

        def focusOut(entry,  isUser):#When entry is clicked out
            if entry.get():
                return False
            entry.config(fg="grey")
            if isUser: entry.insert(0, "Username: ")
            else: entry.insert(0, "Password: ")

        #Username entry:
        self.usernameEntry = tk.Entry(self.frameEntries, borderwidth=5, fg="grey")
        self.usernameEntry.insert(0, "Username: ")
        self.usernameEntry.bind("<FocusIn>", lambda event: focusIn(self.usernameEntry, True))
        self.usernameEntry.bind("<FocusOut>", lambda event: focusOut(self.usernameEntry, True))
        self.usernameEntry.pack()
        
        #Password Entry:
        self.passwordEntry = tk.Entry(self.frameEntries, borderwidth=5, fg="grey")
        self.passwordEntry.insert(0, "Password: ")
        self.passwordEntry.bind("<FocusIn>", lambda event: focusIn(self.passwordEntry, False))
        self.passwordEntry.bind("<FocusOut>", lambda event: focusOut(self.passwordEntry, False))
        self.passwordEntry.pack()

        #Buttons
        #Sign In Button:
        self.signInButton = tk.Button(self.frameButtons, text="Sign In", font=("Helvetica", 20), command=self.signIn)
        self.signInButton.pack(pady=(30,0))

        #Places all the frames inro the screen:
        self.frameTitle.grid(row=0, column=0, columnspan=2)
        self.frameEntries.grid(row=1, column=0)
        self.frameButtons.grid(row=2, column=0, columnspan=2)

    def signIn(self):
        def updateEntries():
            #Gets the input:
            name = self.usernameEntry.get()
            password = self.passwordEntry.get()

            #Deletes the inputs:
            self.usernameEntry.delete(0, "end")
            self.passwordEntry.delete(0, "end")

            return name, password
        
        name, password = updateEntries()

        user = User(name)
        if user.sign_in([], name, password) == None:
            self.errorLabel.config(text="Wrong username or password. Please try again.")
        


    def signUpSection(self, frame):
        #Main Frame:
        self.frameSignUp = tk.Frame(frame)

        ##Text:
        self.textLabel = tk.Label(self.frameSignUp, text="If you do not have an account\n please create one: ")
        self.textLabel.pack(side="left")

        #Button:
        self.signUpButton = tk.Button(self.frameSignUp, text="Sign Up", command= openSignUpWindow)
        self.signUpButton.pack(side="right")

    def kill(self):
        self.root.destroy()

def openSignUpWindow():
    root = tk.Toplevel()
    topApp = SignUpPopUpApp(root)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = SignInPopUpApp(root)
    root.mainloop()