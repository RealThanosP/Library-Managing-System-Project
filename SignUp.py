import tkinter as tk
from User import User

class SignUpPopUpApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x400-1900+200")
        self.root.title("Library Management System")
        self.root.resizable(False, False)

        #Main Frame:
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand= True)

        #Places the Sign in section to the screen
        self.signUpSection(self.frame)
        self.frameSignUp.pack()

        #Error label:
        self.errorLabel = tk.Label(self.frame, text="Errors")
        self.errorLabel.place(relx=0.5, rely=0.95, anchor="s")

    #Sign in section:
    def signUpSection(self, frame):
        '''Handles the visible part where you can sign in to the platform'''
        #Main frame
        self.frameSignUp = tk.Frame(frame)

        #Frame for the entries
        self.frameEntries = tk.Frame(self.frameSignUp)

        #Frame for the buttons
        self.frameButtons = tk.Frame(self.frameSignUp)

        #Frame fo the title label:
        self.frameTitle = tk.Frame(self.frameSignUp)

        #Title Label:
        self.titleLabel = tk.Label(self.frameTitle, text="Make a new account: ", font=("Helvetica", 20))
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
        self.signUpButton = tk.Button(self.frameButtons, text="Sign Up", font=("Helvetica", 20), command=self.signUp)
        self.signUpButton.pack(pady=(30,0))

        #Places all the frames inro the screen:
        self.frameTitle.grid(row=0, column=0, columnspan=2)
        self.frameEntries.grid(row=1, column=0)
        self.frameButtons.grid(row=2, column=0, columnspan=2)

    def signUp(self):
        def updateEntries():
            '''Clears out the entries and returns the username and password'''
            #Gets the input:
            name = self.usernameEntry.get()
            password = self.passwordEntry.get()

            #Deletes the inputs:
            self.usernameEntry.delete(0, "end")
            self.passwordEntry.delete(0, "end")

            return name, password
        name, password = updateEntries()
        
        if name and password:
            user = User(name)
        else:
            self.errorLabel.config(text="Please enter a username and a password")
            return 0
        
        credentials = user.sign_up(name, password)
        if credentials == "Username already taken. Please try again.":
            self.errorLabel.config(text=credentials)
        elif credentials == "Signup successful!":
            self.errorLabel.config(text=credentials)
        else:
            self.errorLabel.config(text="Something went wrong please try again")

if __name__ == "__main__":
    root = tk.Tk()
    app = SignUpPopUpApp(root)
    root.mainloop()