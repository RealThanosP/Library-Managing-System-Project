import tkinter as tk
from tkinter import messagebox
from PIL import Image,ImageTk

class AdminPopUp:
    def __init__(self, root):
        self.BookAttributes = ("Isbn:", "Title:", "Author:", "Section:", "Stock:")
        self.root = root
        self.root.geometry("600x500")
        self.root.title("Admin Menu")
        self.root.resizable(False, True)
        
        #Main frame
        self.frame = tk.Frame(self.root, bg="grey")
        self.frame.pack(expand=True, fill="both")

        #Places the backround of the window
        self.setBackround(self.frame, "background.png")
        #Places the frame of the add book section on the screen
        self.addSection(self.frame)
        self.frameAdd.place(relx=0.25, rely=0.05, anchor="n")

        #Places the frame of the edit book section on the screen
        self.EditSection(self.frame)
        self.frameEdit.place(relx=0.75, rely=0.05, anchor="n")

        #Close button
        self.closeButton = tk.Button(self.frame, text="Close", font=("Helvetica", 20), padx=15, pady=15, command=self.kill)
        self.closeButton.place(relx=0.5, rely=0.99,anchor="s")
    
    def setBackround(self, frame, image):
        #Sets up the backroound
        image = Image.open(image)
        img_w, img_h = image.size
        image = image.resize((700, int(1920*img_h/img_w)))
        self.bg = ImageTk.PhotoImage(image)
        self.backround = tk.Canvas(frame)
        self.backround.create_image(0, 0, image=self.bg, anchor="nw")
        self.backround.pack(fill="both", expand=True)

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
            self.addBookField.pack(pady=4)
        #Adds all the entries to a list to be used later to extract the data:
            self.addBookEntries.append(self.addBookField)
        #Create the pointing labels to the entries:
            self.addBookLabel = tk.Label(self.frameOfLabels, text=self.BookAttributes[i])
            self.addBookLabel.pack(pady=7)

        #Add Button
        self.addButton = tk.Button(self.frameAdd, 
                                    text="Submit", 
                                    pady=15, padx=15,
                                    font=("Helvetica", 20),
                                    command=self.addBook)

        #Error Label at the bottom 
        self.errorLabelAdd = tk.Label(self.frameAdd, text="")

        #Places evry frame on the screen:
        self.topLabel.grid(row=0, column=1, columnspan=2, padx=(0,50))
        self.frameOfLabels.grid(row=1, column=0)
        self.frameOfEntries.grid(row=1, column=1)
        self.addButton.grid(row=2, column=0, columnspan=2)
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
            self.editBookField.pack(pady=4)
        #Adds all the entries to a list to be used later to extract the data:
            self.editBookEntries.append(self.editBookField)
        #Create the pointing labels to the entries:
            self.editBookLabel = tk.Label(self.frameEditLabels, text=self.BookAttributes[i], justify="center")
            self.editBookLabel.pack(pady=7)

        #Find Button
        self.findButton = tk.Button(self.frameEditButtons, text="Find", 
                                    pady=17, padx=12,
                                    font=("Helvetica", 20),
                                    command=self.editBook)
        self.findButton.pack(side="left")

        #Submit Button
        self.submitButton = tk.Button(self.frameEditButtons, text="Submit\nChanges", 
                                    pady=2, padx=10,
                                    font=("Helvetica", 20),
                                    command=self.submitChanges)
        self.submitButton.pack(side="right")

        #Error-Label
        self.errorLabelEdit = tk.Label(self.frameEditError, text="")
        self.errorLabelEdit.pack()

        #Places all the frame in the screen:
        self.frameEditTitle.grid(row=0, column=0, columnspan=2)
        self.frameEditLabels.grid(row=1, column=0)
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
            self.errorLabelEdit.config(text=self.findBook()[2])
  
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
    
    def kill(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminPopUp(root)
    root.mainloop()