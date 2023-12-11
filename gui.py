import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image , ImageTk
from AdminWindow import AdminPopUp
from User import User
from SignUp import SignUpPopUpApp

class SignInPopUpApp:
        
    def __init__(self, root):
        self.name = ""
        self.root = root
        self.root.geometry("300x400-300+200")
        self.root.title("Library Management System")
        self.root.resizable(False, False)

        #Useful placeholders:
        self.placeholders = ("Username: ", "Password: ")

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
            if isUser: entry.config(fg="black")
            else: entry.config(fg="black", show="*")

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
        self.frameEntries.grid(row=1, column=0, columnspan=2)
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
        if user.sign_in([], name, password) == None or name == "Username: ":
            self.errorLabel.config(text="Wrong username or password. Please try again.")
        else:
            self.root.destroy()
            self.name = name
            self.openAppWindow()
            self.errorLabel.config(text=f"Welcome back, {name}")

    def signUpSection(self, frame):
        #Main Frame:
        self.frameSignUp = tk.Frame(frame)

        ##Text:
        self.textLabel = tk.Label(self.frameSignUp, text="If you do not have an account\n please create one: ")
        self.textLabel.pack(side="left")

        #Button:
        self.signUpButton = tk.Button(self.frameSignUp, text="Sign Up", command= self.openSignUpWindow)
        self.signUpButton.pack(side="right")

    def openAppWindow(self):
        master = tk.Tk()
        Main = App(master, self.name)
        master.mainloop()

    def openSignUpWindow(self):
        root = tk.Toplevel()
        topApp = SignUpPopUpApp(root)
        root.mainloop()

class App:
    '''Opens the library App and handles all of it's functionalities'''
    def __init__(self, root, username):
        self.name = username
        self.root = root
        self.root.title("Library Management System") 
        self.root.geometry("600x500-300+100")
        self.root.resizable(False,False)

        #Usefull placeholders and lists
        self.BookAttributes = ("Isbn:", "Title:", "Author:", "Section:", "Stock:")
        self.adminNames = ["admin"]
        
        #Defines the main-frame and packs it into the screen:
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)
        
        #Places backround into the screen
        self.setBackround(self.frame, "background.png", 600, 500)

        #Button to sign out
        self.signoutButton = tk.Button(self.frame, text="↩Sign out", font=("Helvetica", 15), command=self.openSignInWindow)
        self.signoutButton.place(relx=0.01, rely=0.05, anchor="w")

        #Places the User data on the top of the screen
        self.userLabelbg = ImageTk.PhotoImage(Image.open("backcover.png").resize((350,35)))
        self.userLabel = ttk.Label(self.frame, 
                                    image=self.userLabelbg, 
                                    text=f"{self.name}", 
                                    font=("New York Times", 15, "bold italic"),
                                    borderwidth=0,
                                    relief="sunken",
                                    compound="center"
                                    )
        self.userLabel.place(relx=0.99, rely=0.05, anchor="e")
        

        #Place the frame of the loan a book section on the screen
        self.LoanSection(self.frame)
        self.frameLoan.place(relx=0.25, rely=0.15, anchor="n")

        #Places the frame of the return book section on the screen
        self.ReturnSection(self.frame)
        self.frameReturn.place(relx=0.75, rely=0.15, anchor="n")

        #Decides weather to place a book to access the database
        if self.name in self.adminNames:
            self.changeLibraryButton = tk.Button(self.frame, text="Make Changes", font=("Helvetica",15),padx=15, pady=15, command=self.openAdminWindow)
            self.changeLibraryButton.place(relx=0.5, rely=0.9, anchor="s")

    def setBackround(self, frame, image, width, height):
        #Sets up the backroound
        image = Image.open(image)
        img_w, img_h = image.size
        image = image.resize((width, height))
        self.bg = ImageTk.PhotoImage(image)
        self.backround = tk.Canvas(frame, border=0, highlightthickness=0, relief="ridge")
        self.backround.create_image(0, 0, image=self.bg, anchor="nw")
        self.backround.place(x=0, y=0, relwidth=1, relheight=1)
    
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
                                font=("Helvetica",20),
                                pady=10)
        self.loanLabel.pack()

        #Loan Book Entries for searching the book in the database based on [isbn OR (title AND author)]
        for i in range(3):
            #Entries
            self.loanEntry = tk.Entry(self.frameLoanEntries, borderwidth=5, width=25)
            self.loanEntry.pack(pady=4)

            #Entry list to manage their info seperately
            self.loanBookEntries.append(self.loanEntry)

            #The labels for the entries
            self.entryLabel = tk.Label(self.frameLoanLabels, text=self.BookAttributes[i], justify="center") 
            self.entryLabel.pack(pady=8)

        #The find Button
        self.loanFindButton = tk.Button(self.frameLoanButtons, text="Find", 
                                        pady=16, padx=12,
                                        bg="#CFCFCF",
                                        font=("Helvetica", 20),
                                        command=lambda: print(self.findBook))########### CHANGE THE FUNCTION
        self.loanFindButton.pack(side="left", padx=(10,5))

        #The Submit Button
        self.loanSubmitButton = tk.Button(self.frameLoanButtons, text="Submit\nLoan", 
                                    pady=0, padx=15,
                                    bg="#CFCFCF",
                                    font=("Helvetica", 20),
                                    command=lambda: print(self.findbook))############# CHANGE THE FUNCTIONS
        self.loanSubmitButton.pack(side="right", padx=(5,10))

        #Error Label
        self.errorLabelLoan = tk.Label(self.frameLoanErrors, text="Error Label")
        self.errorLabelLoan.grid(row=5, column=0, columnspan=2, pady=1)

        #Places all the frames into the screen
        self.frameLoanTitle.grid(row=0,column=0,columnspan=2)
        self.frameLoanLabels.grid(row=1, column=0)
        self.frameLoanEntries.grid(row=1,column=1)
        self.frameLoanButtons.grid(row=2,column=0,columnspan=2)
        self.frameLoanErrors.grid(row=3,column=0,columnspan=2)
    
    #Return Book Frame
    def ReturnSection(self, frame):
        #Main Frame
        self.returnBookEntries = []
        self.frameReturn = tk.Frame(frame)
        
        #Title frame
        self.frameReturnTitle = tk.Frame(self.frameReturn)

        #Entries frame
        self.frameReturnEntries = tk.Frame(self.frameReturn)

        #Label Frame
        self.frameReturnLabels = tk.Frame(self.frameReturn)

        #Buttons frame
        self.frameReturnButton = tk.Frame(self.frameReturn)

        #Title Label
        self.returnTitle = tk.Label(self.frameReturnTitle, 
                                    text="Return your Book", 
                                    font=("Helvetica", 20),
                                    pady=10) 
        self.returnTitle.pack()

        #Title and author inputs
        for i in range(2):
            #Labels
            self.returnBookLabel = tk.Label(self.frameReturnLabels, text=self.BookAttributes[i+1]) 
            self.returnBookLabel.pack(pady=8)

            #Entries
            self.returnBookEntry = tk.Entry(self.frameReturnEntries, borderwidth=5, width=25)
            self.returnBookEntry.pack(pady=5)

            self.returnBookEntries.append(self.returnBookEntry)


        #Return Button (Checks if it exists and submits the changes)
        self.returnButton = tk.Button(self.frameReturnButton, 
                                        text="Return", 
                                        pady=15, padx=15,
                                        font=("Helvetica", 20), 
                                        bg="#CFCFCF")
        self.returnButton.pack()

        #Error Label
        self.errorLabelReturn = tk.Label(self.frameReturn, text="ERROR")

        #Places everything on the main frame
        self.frameReturnTitle.grid(row=0, column=0, columnspan=2)
        self.frameReturnLabels.grid(row=1, column=0, padx=10)
        self.frameReturnEntries.grid(row=1, column=1, padx=10)
        self.frameReturnButton.grid(row=2, column=0, columnspan=2)
        self.errorLabelReturn.grid(row=3, column=0, columnspan=2)

    def findBook(self):
        '''Main search function. Returns tuple: (isFound, string of the book found)'''
        #Gets the inputs form the entries
        isbn = self.editBookEntries[0].get()
        title = self.editBookEntries[1].get()
        author = self.editBookEntries[2].get()
        section = self.editBookEntries[3].get()
        stock = self.editBookEntries[4].get()
        error = ""#Controls the text shown to the user based on if book is found
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
                    if found: 
                        error = "Book Found"
                        break
                except IndexError: 
                    error = "This book is not in our library's database"
        return found, book, error

    def openAdminWindow(self):
        master = tk.Toplevel()
        app = AdminPopUp(master)
        master.mainloop()
    
    def openSignInWindow(self):
        self.root.destroy()
        root = tk.Tk()
        app = SignInPopUpApp(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = SignInPopUpApp(root)
    root.mainloop()