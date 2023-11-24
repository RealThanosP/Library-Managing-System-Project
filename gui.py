from tkinter import *


class App:
    add_book_entries = []
    loan_book_entries = []

    add_placeholder = ("Isbn:", "Title:", "Author:", "Summary:", "Stock:")
    loan_placeholder = ("Find by Isbn:", "Find by Title:")
    def __init__(self, root):
        self.root = root
        root.title("Library Management System")
        root.geometry("900x900")
    #Defines the main-frame and packs it into the screen:
        self.frame = Frame(root)
        self.frame.pack()

#Search-bar-section:
    #Search-bar:
        self.search_bar = Entry(self.frame, borderwidth=5, width = 90)
        self.search_bar.grid(row=0, column=0, columnspan=5)

    #Search-button:
        self.search_button = Button(self.frame, text="Search")
        self.search_button.grid(row=0, column=5)

#Adding-book-section:
    #Add-a-book-button
        self.add_button = Button(self.frame, text="Add Book", command=self.add_book_database)
        self.add_button.grid(row=1, column=0, columnspan=2)
    #Error-text-label:
        self.error_label = Label(self.frame)
        self.error_label.grid(row=7,column=0, columnspan=2)
    #The inputs for the atributes of the new book:
        for i in range(0,5):
        #Creates 5 input fielsds to fill:
            self.input_book = Entry(self.frame, borderwidth=5, width=25)
            self.input_book.grid(row=i+2, column=1, sticky="w")
        #Adds all the entries to a list to be used later to extract the data:
            self.add_book_entries.append(self.input_book)
        #Create the pointing labels to the entries:
            self.add_book_label = Label(self.frame, text=self.add_placeholder[i], justify="right", width= 2)
            self.add_book_label.grid(row=i+2, column=0, sticky="we")

#Loaning-book-section:
    #Loan-book-button
        self.loan_button = Button(self.frame, text="Loan")
        self.loan_button.grid(row=1, column=2,columnspan=2)
    #Loan-labels:
        for i in range(2,4):
            self.loan_label = Label(self.frame, text=self.loan_placeholder[i-2],width=4)
            self.loan_label.grid(row=i, column=2, sticky="we")
    
    #Loan-book-field:
        for i in range(2,4):
            self.loan_input = Entry(self.frame, borderwidth=5, width=25)
            self.loan_input.grid(row=i,column=3,sticky="w")
            self.loan_book_entries.append(self.loan_input)
            
#Return-book-section:
    #Return-button:
        self.return_button = Button(self.frame, text="Return")
        self.return_button.grid(row=1, column=4)

#kill button (for develiping purposes only)
        self.kill = Button(self.frame, text="KILL", font=("Ariel", 20), command=self.kill)
        self.kill.grid(row=10, column=0, columnspan=10)

    def kill(self):
        self.root.destroy()

    #Adds a new book to the database every time "Add book" button is being pressed:
    def add_book_database(self):
        book_data = ""
    #Takes the inputs of the 5 entries and stores them into a string with commas:
        for i in range(5):
            book_data += self.add_book_entries[i].get() + ","
            self.add_book_entries[i].delete(0,END)
        
        book_data = book_data.split(",")
        try:
        #Checks the input's correctness:
            isbn = int(book_data[0])
            title = book_data[1]
            author = book_data[2]
            summary = book_data[3]
            stock = int(book_data[4])
        #Just makes sure isbn and the remaining items are integers:
        except ValueError:
            self.error_label.config(text="The isbn or the total stock inputs are invalid, Try again: ")
        
        if len(str(isbn).strip(" ")) == 13:
                #try:
                #Takes the inputs to a list and then passes them into database.txt:
            atributes = [str(isbn), title, author, summary, str(stock)]
            book = "(|)".join(atributes) + "\n"

                #Passes the data to the databases part:
            database = open("database.txt", "a", encoding="utf-8")
            database.write(book)
            database.close()
            self.error_label.config(text="Book Added ✔️")
        
        else:
            text_error = f"The isbn input is invalid, Try again: {str(isbn).strip(' ')}"
            self.error_label.config(text=text_error)
        
    def search(self):
        #Search button function
        return


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
