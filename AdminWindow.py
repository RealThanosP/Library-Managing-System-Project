import tkinter as tk
from tkinter import messagebox
from PIL import Image,ImageTk
from database import Database, Book
bg=""

class AdminPopUp:

    def __init__(self, root):
        self.BookAttributes = ("Isbn:", "Title:", "Author:", "Section:", "Stock:")
        self.root = root
        self.root.geometry("900x500")
        self.root.title("Admin Menu")
        self.root.resizable(False, False)
        
        #Main frame
        self.frame = tk.Frame(self.root, bg="grey")
        self.frame.pack(expand=True, fill="both")

        #Places the backround of the window
        self.setBackround(self.frame, "background.png", 900, 500)
        #Places the frame of the add book section on the screen
        self.addSection(self.frame)
        self.frameAdd.place(relx=0.2, rely=0.05, anchor="n")

        #Places the frame of the edit book section on the screen
        self.editSection(self.frame)
        self.frameEdit.place(relx=0.55, rely=0.05, anchor="n")

        #Places the frame of the user management section
        self.userSection(self.frame)
        self.frameUser.place()

        #Close button
        self.closeButton = tk.Button(self.frame, text="Close", font=("Helvetica", 20), padx=15, pady=15, command=self.kill)
        self.closeButton.place(relx=0.5, rely=0.99,anchor="s")
    
    def setBackround(self, frame, image, width, height):
        #Sets up the backroound
        image = Image.open(image)
        img_w, img_h = image.size
        image = image.resize((width, height))
        self.bg = ImageTk.PhotoImage(image)
        self.backround = tk.Canvas(frame, highlightthickness=0, relief="ridge", border=0)
        self.backround.create_image(0, 0, image=self.bg, anchor="nw")
        self.backround.pack(fill="both", expand=True)

    #Add Book Frame
    def addSection(self, frame):
        #Main frame:
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
        self.errorLabelAdd = tk.Label(self.frameAdd, text="", bg="#D2B48C")

        #Places evry frame on the screen:
        self.topLabel.grid(row=0, column=1, columnspan=2, padx=(0,70), pady=10)
        self.frameOfLabels.grid(row=1, column=0)
        self.frameOfEntries.grid(row=1, column=1)
        self.addButton.grid(row=2, column=0, columnspan=2, pady=(20,0))
        self.errorLabelAdd.grid(row=3, column=0, columnspan=2, pady=(6,0))

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
            if check == "This book is already in the database.\n You can edit it's details on the other window.":
                self.errorLabelAdd.config(text=check)
            elif check == 'Book successfully added!':
                messagebox.showinfo(title="Adding Books", message="Book Added ✔")
                self.errorLabelAdd.config(text="")
            else:
                self.errorLabelAdd.config(text=check)

        #Just makes sure isbn and the remaining items are integers:
        except ValueError:
            self.errorLabelAdd.config(text="The data you entered are invalid\n Try again: ")
            
    #Edit Book Frame
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

        #Find Button
        self.findButton = tk.Button(self.frameEditButtons, text="Find", 
                                    pady=17, padx=12,
                                    font=("Helvetica", 20),
                                    bg="#CFCFCF",
                                    command=self.editBook)
        self.findButton.pack(side="left")

        #Submit Button
        self.submitButton = tk.Button(self.frameEditButtons, text="Submit\nChanges", 
                                    pady=2, padx=10,
                                    font=("Helvetica", 20),
                                    bg="#CFCFCF",
                                    command=self.submitChanges)
        self.submitButton.pack(side="right")

        #Error-Label
        self.errorLabelEdit = tk.Label(self.frameEditError, text="", bg="#D2B48C")
        self.errorLabelEdit.pack()

        #Places all the frame in the screen:
        self.frameEditTitle.grid(row=0, column=0, columnspan=2)
        self.frameEditLabels.grid(row=1, column=0)
        self.frameEditEntries.grid(row=1, column=1)
        self.frameEditButtons.grid(row=2,column=0,columnspan=2, pady=(20,0))
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
    
    def userSection(self, frame):
        "Handles the frame of the user Management Section"
        #Main frame
        self.frameUser = tk.Frame(frame)

        #Title frame
        self.frameUserTitle = tk.Frame(self.frameUser)
        self.userTitleLabel = tk.Label(self.frameUser, text="User \nManagement", font=("Helvetica", 18))
        
        #Menu to see all the users and edit their privileges

        #Checkboxes for the admin privileges
        
        #Text with the book of it's user on the side

        #Submit button

        #Error label
     
    def kill(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminPopUp(root)
    root.mainloop()