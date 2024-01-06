import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image , ImageTk
from AdminWindow import AdminPopUp
from User import User   
from SignUp import SignUpPopUpApp
from database import Book, Database
from SeeYourBooks import BookDisplay
import os

class SignInPopUpApp:
    '''Small window that handles the signIn/Up process for the users of the library'''
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

        #Set the backround
        self.setBackround(self.frame, "background.png", 300, 400)

        #Places the Sign in section to the screen
        self.signInSection(self.frame)
        self.frameSignIn.pack(pady=(30,0))

        self.root.bind('<Return>', lambda event: self.signIn(event))

        #Frame for the bottom text
        self.signUpSection(self.frame)
        self.frameSignUp.place(relx=0.5, rely=0.9, anchor="center")

    def signInSection(self, frame):
        '''Handles the visible part where you can sign in to the platform'''
        #Main frame
        self.frameSignIn = tk.Frame(frame, bg="#D2B48C")

        #Frame for the entries
        self.frameEntries = tk.Frame(self.frameSignIn, bg="#D2B48C")

        #Frame for the buttons
        self.frameButtons = tk.Frame(self.frameSignIn, bg="#D2B48C")

        #Frame fo the title label:
        self.frameTitle = tk.Frame(self.frameSignIn, bg="#D2B48C")

        #Title Label:
        self.titleLabel = tk.Label(self.frameTitle, 
                                    text="Join the App!!!", 
                                    font=("Helvetica", 20),
                                    bg="#C7A186")
        self.titleLabel.pack(pady=(20,60), padx=25)

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
        self.usernameEntry = tk.Entry(self.frameEntries, borderwidth=5, fg="grey", width=25)
        self.usernameEntry.insert(0, "Username: ")
        self.usernameEntry.bind("<FocusIn>", lambda event: focusIn(self.usernameEntry, True))
        self.usernameEntry.bind("<FocusOut>", lambda event: focusOut(self.usernameEntry, True))
        self.usernameEntry.pack()
        
        #Password Entry:
        self.passwordEntry = tk.Entry(self.frameEntries, borderwidth=5, fg="grey", width=25)
        self.passwordEntry.insert(0, "Password: ")
        self.passwordEntry.bind("<FocusIn>", lambda event: focusIn(self.passwordEntry, False))
        self.passwordEntry.bind("<FocusOut>", lambda event: focusOut(self.passwordEntry, False))
        self.passwordEntry.pack()

        #Buttons
        #Sign In Button:
        self.signInButton = tk.Button(self.frameButtons, text="Sign In", font=("Helvetica", 20))
        self.signInButton.bind("<Button-1>", lambda event: self.signIn(event))
        self.signInButton.pack(pady=(30,0))

        #Error Label
        self.errorLabel = tk.Label(self.frameSignIn, bg="#D2B48C")

        #Places all the frames inro the screen:
        self.frameTitle.grid(row=0, column=0, columnspan=2)
        self.frameEntries.grid(row=1, column=0, columnspan=2)
        self.frameButtons.grid(row=2, column=0, columnspan=2)
        self.errorLabel.grid(row=3, column=0, columnspan=2)
    
    def updateEntries(self):
            #Gets the input:
            name = self.usernameEntry.get()
            password = self.passwordEntry.get()

            #Deletes the inputs:
            self.usernameEntry.delete(0, "end")
            self.passwordEntry.delete(0, "end")

            return name, password
    
    def signIn(self, event):
        
        name, password = self.updateEntries()

        user = User(name)
        if user.sign_in(name, password) == None or name == "Username: ":
            self.errorLabel.config(text="Wrong username or password.\nPlease try again.")
        else:
            self.root.destroy()
            self.name = name
            self.openAppWindow()
            
    def signUpSection(self, frame):
        #Main Frame:
        self.frameSignUp = tk.Frame(frame)

        ##Text:
        self.textLabel = tk.Label(self.frameSignUp, text="If you do not have an account\n please create one: ")
        self.textLabel.pack(side="left")

        #Button:
        self.signUpButton = tk.Button(self.frameSignUp, text="Sign Up", command= self.openSignUpWindow)
        self.signUpButton.pack(side="right")
    
    def setBackround(self, frame, image, width, height):
        #Sets up the backroound
        image = Image.open(image)
        img_w, img_h = image.size
        image = image.resize((width, height))
        self.bg = ImageTk.PhotoImage(image)
        self.backround = tk.Canvas(frame, border=0, highlightthickness=0, relief="ridge")
        self.backround.create_image(0, 0, image=self.bg, anchor="nw")
        self.backround.place(x=0, y=0, relwidth=1, relheight=1)

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

        #Initiate the user info and the database state:
        self.user = User(self.name)
        self.library = Database("Library.db")

        #Usefull placeholders and lists
        self.BookAttributes = ("Isbn:", "Title:", "Author:", "Section:", "Stock:")
        self.adminNames = ["admin"]
        
        #Defines the main-frame and packs it into the screen:
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)
        
        #Places backround into the screen
        self.setBackround(self.frame, "background.png", 600, 500)

        #Button to sign out
        self.signoutButton = tk.Button(self.frame, text="↩Sign out", font=("Helvetica", 15), bg="#CFCFDF",command=self.openSignInWindow)
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

        #Button that lets you access your books
        self.yourBookButton = tk.Button(self.frame, 
                            text="Your Books", 
                            font=("Helvetica, 15"),
                            bg="#CFCFDF",
                            padx=15,pady=15,
                            command=self.openBookList)
        self.yourBookButton.place(relx=0.2, rely=0.9, anchor="s")

        #Button that lets you browse the library and loan books easier
        self.browseBooksButton = tk.Button(self.frame, 
                            text="Browse...", 
                            font=("Helvetica, 15"),
                            bg="#CFCFDF",
                            padx=15,pady=15,
                            command=self.openBrowseWindow)
        self.browseBooksButton.place(relx=0.8, rely=0.9, anchor="s")

        #Decides weather to place a button to access the database
        if self.name in self.adminNames:
            self.changeLibraryButton = tk.Button(self.frame, 
                                            text="Make Changes", 
                                            font=("Helvetica",15), 
                                            bg="#CFCFDF",
                                            padx=15, pady=15, 
                                            command=self.openAdminWindow)
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
    
    def LoanSection(self, frame):
        self.loanBookEntries = []
        #Defines the main frame
        self.frameLoan = tk.Frame(frame, bg="#D2B48C")

        #Frame for the title:
        self.frameLoanTitle = tk.Frame(self.frameLoan, bg="#D2B48C")

        #Frame for the entries:
        self.frameLoanEntries = tk.Frame(self.frameLoan, bg="#D2B48C")

        #Frame for the labels:
        self.frameLoanLabels = tk.Frame(self.frameLoan, bg="#D2B48C")

        #Frame for the buttons
        self.frameLoanButtons = tk.Frame(self.frameLoan, bg="#D2B48C")

        #Frame for the error label
        self.frameLoanErrors = tk.Frame(self.frameLoan, bg="#D2B48C")
        
        #Title Label
        self.loanLabel = tk.Label(self.frameLoanTitle, 
                                text="Loan a Book", 
                                justify="center",
                                font=("Helvetica",20),
                                pady=10, bg="#D2B48C")
        self.loanLabel.pack()

        #Loan Book Entries for searching the book in the database based on [isbn OR (title AND author)]
        for i in range(2):
            #Entries
            self.loanEntry = tk.Entry(self.frameLoanEntries, borderwidth=5, width=25)
            self.loanEntry.pack(pady=4)

            #Entry list to manage their info seperately
            self.loanBookEntries.append(self.loanEntry)

            #The labels for the entries
            self.entryLabel = tk.Label(self.frameLoanLabels, text=self.BookAttributes[i+1], justify="center", bg="#D2B48C") 
            self.entryLabel.pack(pady=8)

        #The Submit Button
        self.loanSubmitButton = tk.Button(self.frameLoanButtons, text="Loan", 
                                    pady=15, padx=20,
                                    bg="#CFCFDF",
                                    font=("Helvetica", 20),
                                    command=self.loanBook)############# CHANGE THE FUNCTIONS
        self.loanSubmitButton.pack(side="right", padx=(5,10))

        #Error Label
        self.errorLabelLoan = tk.Label(self.frameLoanErrors, text="", bg="#D2B48C")
        self.errorLabelLoan.grid(row=5, column=0, columnspan=2, pady=1)

        #Places all the frames into the screen
        self.frameLoanTitle.grid(row=0,column=0,columnspan=2)
        self.frameLoanLabels.grid(row=1, column=0,padx=10)
        self.frameLoanEntries.grid(row=1,column=1,padx=10)
        self.frameLoanButtons.grid(row=2,column=0,columnspan=2, pady=10)
        self.frameLoanErrors.grid(row=3,column=0,columnspan=2)
    
    def loanBook(self):
        '''Allows the find button to find the book ot be loaned out'''
        title = self.loanBookEntries[0].get()
        author = self.loanBookEntries[1].get()
        
        #Update the entries
        for index, entry in enumerate(self.loanBookEntries):
            entry.delete(0, "end")

        #Search for the book:
        found_book = self.library.get_book(0, title, author)#tuple
        
        if found_book == None:
            self.errorLabelLoan.config(text="The book you ask for is not in our database")  
            return
        
        #Set the book
        book = Book(*found_book)

        if book.stock > 0:
            loan_book = self.user.loan_out(book)

            if loan_book == None:
                self.errorLabelLoan.config(text="You already have the book loaned out")
                return

            book.stock -= 1
            self.library.updateInfo(book.isbn, book.title, book.author, book.section, book.stock)
            self.errorLabelLoan.config(text=f"You loaned out {book.title} by {book.author}.\nEnjoy it")
        else:
            self.errorLabelLoan.config(text=f"We are sorry but, {book.title} by {book.author} is out of stock")#f"We are sorry but {book.title} by {book.author}\n is out of stock")
        
    def openBookList(self):
        root = tk.Toplevel()
        app = BookDisplay(root, self.name)
        root.mainloop

    def ReturnSection(self, frame):
        #Main Frame
        self.returnBookEntries = []
        self.frameReturn = tk.Frame(frame, bg="#D2B48C")
        
        #Title frame
        self.frameReturnTitle = tk.Frame(self.frameReturn, bg="#D2B48C")

        #Entries frame
        self.frameReturnEntries = tk.Frame(self.frameReturn, bg="#D2B48C")

        #Label Frame
        self.frameReturnLabels = tk.Frame(self.frameReturn, bg="#D2B48C")

        #Buttons frame
        self.frameReturnButton = tk.Frame(self.frameReturn, bg="#D2B48C")

        #Title Label
        self.returnTitle = tk.Label(self.frameReturnTitle, 
                                    text="Return your Book", 
                                    font=("Helvetica", 20),
                                    pady=10, bg="#D2B48C") 
        self.returnTitle.pack()

        #Title and author inputs
        for i in range(2):
            #Labels
            self.returnBookLabel = tk.Label(self.frameReturnLabels, text=self.BookAttributes[i+1], bg="#D2B48C") 
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
                                        bg="#CFCFDF",
                                        command=self.returnBook)
        self.returnButton.pack()

        #Error Label
        self.errorLabelReturn = tk.Label(self.frameReturn, text="", bg="#D2B48C")

        #Places everything on the main frame
        self.frameReturnTitle.grid(row=0, column=0, columnspan=2)
        self.frameReturnLabels.grid(row=1, column=0, padx=10)
        self.frameReturnEntries.grid(row=1, column=1, padx=10)
        self.frameReturnButton.grid(row=2, column=0, columnspan=2, pady=10)
        self.errorLabelReturn.grid(row=3, column=0, columnspan=2)

    def returnBook(self):
        '''Returns the book in the database'''
        #Gets the details of the book:
        title = self.returnBookEntries[0].get()
        author = self.returnBookEntries[1].get()

        #Update the entries
        for index, entry in enumerate(self.returnBookEntries):
            entry.delete(0, "end")

        #Search for the book
        found_book = self.library.get_book(0, title, author)

        if found_book == None:
            self.errorLabelReturn.config(text="Something went wrong please try returning your book\nthrough the 'Browse...' menu")
            return 
        
        book = Book(*found_book)
        returning_book = self.user.return_in(book)
        if returning_book == None:
            self.errorLabelReturn.config(text="You haven't loaned out the book to return it")
            return
        
        book.stock += 1
        self.library.updateInfo(book.isbn, book.title, book.author, book.section, book.stock)
        self.errorLabelReturn.config(text=f"You returned '{book.title} by {book.author}' successfully")


    def openAdminWindow(self):
        master = tk.Toplevel()
        app = AdminPopUp(master, self.name)
        master.mainloop()
    
    def openSignInWindow(self):
        self.root.destroy()
        root = tk.Tk()
        app = SignInPopUpApp(root)
        root.mainloop()

    def openBrowseWindow(self):
        name = self.name
        self.root.destroy()
        root = tk.Tk()
        app = BrowseLibrary(root, name)
        root.mainloop()

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
        self.tableUser.column("Author", width=150, minwidth=80)
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
                                       command=self.openMainMenu)
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
                data = line.strip().split("\t\t")
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
            if returned_book == None:
                self.errorLabel.config(text="You haven't loaned out this book to return it.")
                return
            book.stock += 1
            self.library.updateInfo(book.isbn, book.title, book.author, book.section, book.stock)
            self.errorLabel.config(text=f"You successfully returned {book.title} by {book.author}.\nThank you for the preference")
            self.refresh_tables()

    def openMainMenu(self):
        self.root.destroy()
        root = tk.Tk()
        app = App(root, self.name)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = SignInPopUpApp(root)
    root.mainloop()     