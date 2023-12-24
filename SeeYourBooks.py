import tkinter as tk
from tkinter import ttk

class BookDisplay:
    def __init__(self, root, username):
        self.name = username
        self.root = root
        self.root.minsize(800,300)
        self.root.title(f"Book of {self.name}")
        self.tree = ttk.Treeview(self.root, columns=("ISBN", "Title", "Author", "Section"), show="headings")

        #Puts the heading on the table
        #The commands make it so the headings are essetially buttons that user can press
        #to sort the table by column chosen.
        self.tree.heading("ISBN", text="ISBN", command=lambda: self.sort_column("ISBN", False))
        self.tree.heading("Title", text="Title", command=lambda: self.sort_column("Title", False))
        self.tree.heading("Author", text="Author", command=lambda: self.sort_column("Author", False))
        self.tree.heading("Section", text="Section", command=lambda: self.sort_column("Section", False))

        self.tree.pack(expand=True, fill="both")
       
        #Populate the table
        self.tableFill()

    def tableFill(self):
        with open(f"UserFiles/{self.name}.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip().split("\t\t")
                self.tree.insert("", "end", value=line)

    def sort_column(self, column, reverse):
        data = [(self.tree.set(child, column), child) for child in self.tree.get_children("")]
        data.sort(reverse=reverse)

        for index, (val, child) in enumerate(data):
            self.tree.move(child, "", index)

        self.tree.heading(column, command=lambda: self.sort_column(column, not reverse))

if __name__ == "__main__":
    root = tk.Tk()
    app = BookDisplay(root, "admin")
    root.mainloop()