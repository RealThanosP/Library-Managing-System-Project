import tkinter as tk
from User import User
from PIL import Image,ImageTk

class SignUpPopUpApp:
    '''Opens the sign up window'''
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x400+1000+200")
        self.root.title("Library Management System")
        self.root.resizable(False, False)

        #Main Frame:
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand= True)

        self.setBackround(self.frame, "background.png", 300, 400)

        #Places the Sign in section to the screen
        self.signUpSection(self.frame)
        self.frameSignUp.pack(pady=30)

        #Error label:")
        self.errorLabel = tk.Label(self.frame, bg="#D2B48C", text="")
        self.errorLabel.place(relx=0.5, rely=0.95, anchor="s")

    #Sign in section:
    def signUpSection(self, frame):
        '''Handles the visible part where you can sign in to the platform'''
        #Main frame
        self.frameSignUp = tk.Frame(frame, bg="#D2B48C")

        #Frame for the entries
        self.frameEntries = tk.Frame(self.frameSignUp, bg="#D2B48C")

        #Frame for the buttons
        self.frameButtons = tk.Frame(self.frameSignUp, bg="#D2B48C")

        #Frame fo the title label:
        self.frameTitle = tk.Frame(self.frameSignUp, bg="#D2B48C")

        #Title Label:
        self.titleLabel = tk.Label(self.frameTitle, text="Make \na new account: ", font=("Helvetica", 20), bg="#C7A186")
        self.titleLabel.pack(pady=(20,60), padx=15)

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
        self.signUpButton = tk.Button(self.frameButtons, text="Sign Up", font=("Helvetica", 20), command=self.signUp)
        self.signUpButton.pack(pady=(30,30))

        #Places all the frames inro the screen:
        self.frameTitle.grid(row=0, column=0, columnspan=2)
        self.frameEntries.grid(row=1, column=0, columnspan=2)
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
        elif name == "Username: " or password == "Password: ":
            self.errorLabel.place(relx=0.5, rely=0.95, anchor="s")
            self.errorLabel.config(text="Please enter a username and a password")
            return 0

        try: credentials = user.sign_up(name, password)
        except UnboundLocalError: return 0
        
        if credentials == "Username already taken. Please try again.":
            self.errorLabel.config(text=credentials)
        elif credentials == "Signup successful!":
            self.errorLabel.config(text=credentials)
        else:
            self.errorLabel.config(text="Something went wrong please try again")

    def setBackround(self, frame, image, width, height):
        #Sets up the backroound
        image = Image.open(image)
        img_w, img_h = image.size
        image = image.resize((width, height))
        self.bg = ImageTk.PhotoImage(image)
        self.backround = tk.Canvas(frame, border=0, highlightthickness=0, relief="ridge")
        self.backround.create_image(0, 0, image=self.bg, anchor="nw")
        self.backround.place(x=0, y=0, relwidth=1, relheight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = SignUpPopUpApp(root)
    root.mainloop()