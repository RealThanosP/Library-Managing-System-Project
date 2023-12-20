import tkinter as tk
from tkinter import ttk
from database import Database, Book

class BookBrowsing:
    def __init__(self, root, username):
        self.name = username
        self.root = root
        self.root.minsize(800,300)
        self.root.geometry("800x500")
        self.root.title(f"Our Library")
        
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        #Main tree
        self.tree = ttk.Treeview(self.frame, columns=("ISBN", "Title", "Author", "Section", "Stock"), show="headings")


        #Puts the heading on the table
        #The commands make it so the headings are essetially buttons that user can press
        #to sort the table by column chosen.
        self.tree.heading("ISBN", text="ISBN", command=lambda: self.sort_column("ISBN", False))
        self.tree.heading("Title", text="Title", command=lambda: self.sort_column("Title", False))
        self.tree.heading("Author", text="Author", command=lambda: self.sort_column("Author", False))
        self.tree.heading("Section", text="Section", command=lambda: self.sort_column("Section", False))
        self.tree.heading("Stock", text="Stock", command=lambda: self.sort_column("Stock", False))

        self.tree.pack(expand=True, fill="both")
        
        self.frameButtons = tk.Frame(self.root)
        self.frameButtons.pack(side="right", expand=True)

        #Population of the table    
        self.tableFill()

    def sort_column(self, column, reverse):
        data = [(self.tree.set(child, column), child) for child in self.tree.get_children("")]
        data.sort(reverse=reverse)

        for index, (val, child) in enumerate(data):
            self.tree.move(child, "", index)

        self.tree.heading(column, command=lambda: self.sort_column(column, not reverse))
    
    def tableFill(self):
        #Initialize the library
        library = Database("Library.db")
        book_list = library.show_database()

        for book in book_list:
            #Inserts the values
            self.tree.insert("", "end", value=book)

if __name__ == "__main__":
    root  = tk.Tk()
    app = BookBrowsing(root, "admin")
    root.mainloop()