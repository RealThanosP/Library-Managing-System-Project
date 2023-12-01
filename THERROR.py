import tkinter as tk
from tkinter.ttk import *
class EditBookPopApp:
    '''Edit Book pop-up window'''
    add_placeholder = ("Isbn:", "Title:", "Author:", "Section:", "Stock:")
    editBookEntries = []
    def __init__(self, root):
        
        self.root = root
        self.root.title("Edit Book Info")
        self.root.geometry("270x300")

        #Main frame:
        self.frame = tk.Frame(self.root)
        self.frame.pack()

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
        self.findButton.grid(row=6,column=0, columnspan=2)

    def editBook(self):

        def updateEntries(book):
            #Deletes whatever you wrote
            for i in range(0, len(self.editBookEntries)):
                self.editBookEntries[i].delete(0, "end")

            #Prints the info from database on the entries
            for entryIndex, attribute in enumerate(book):
                self.editBookEntries[entryIndex].insert(0, attribute)

        def findBook():
            #Just for the example
            return True, [1234, "Harry Potter", "D.Rowling", 101, 1]
            
        #If the book is found then it just updates the Entries to the current book data
        if findBook()[0]:
            bookInfoList = findBook()[1]
            updateEntries(bookInfoList)
        self.root.destroy()

class App:
    '''Main user-Interface'''
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x500")

        self.button = tk.Button(self.root, text="New Window", command=self.openWindow)
        self.button.pack()

    def openWindow(self):
        master = tk.Toplevel(self.root)
        PopApp = EditBookPopApp(master)
        master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
