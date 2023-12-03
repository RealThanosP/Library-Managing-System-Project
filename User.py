class User:
    def __init__(self, username):
        self.username = username
        self.loans = []  # Each element is a dictionary {'book': book_info, 'loaned_by': username}
        self.library = []  # Each user has their own library

    def myHash(self, text:str):
        hash=0
        for ch in text:
            hash = ( hash*281  ^ ord(ch)*997) & 0xFFFFFFFF
        return str(hash)

    def sign_up(self, username, password):
        passwordHash = self.myHash(password)
        with open("users.txt", "r") as file:
            for line in file:
                existing_username = line.strip().split(',')[0]
                if existing_username == username:
                    return "Username already taken. Please try again."

        with open("users.txt", "a") as file:
            file.write(f"{username},{passwordHash}\n")
        return "Signup successful!"

    def sign_in(self, library, username, password):
        passwordHash = self.myHash(password)

        with open("users.txt", "r") as file:
            for line in file:
                existing_username, existing_password = line.strip().split(',')
                if existing_username == username and existing_password.strip() == passwordHash:
                    print(f"Welcome back, {username}!")
                    self.library = library.copy() 
                    return username
        print("Wrong username or password. Please try again.")
        return None

    def loan_out(self, title, author):
        for book in self.library:
            if book['title'] == title and book['author'] == author and book['stock'] > 0:
                book['stock'] -= 1
                loan_info = {'book': book, 'loaned_by': self.username}
                self.loans.append(loan_info)
                print(f"Book '{title}' by {author} loaned successfully by {self.username}")
                return True
        print(f"Book '{title}' by {author} not available for loan.")
        return False

    def return_in(self, title, author):
        for loan_info in self.loans:
            if loan_info['book']['title'] == title and loan_info['book']['author'] == author:
                if loan_info['loaned_by'] == self.username:
                    book = loan_info['book']
                    book['stock'] += 1
                    self.loans.remove(loan_info)
                    print(f"Book '{title}' by {author} returned successfully by {self.username}")
                    return True
                else:
                    print(f"You can't return a book loaned by another user.")
                    return False
        print(f"Book '{title}' by {author} not found in the user's loans.")
        return False

    def display_loans(self):
        print(f"{self.username}'s Loans:")
        for loan_info in self.loans:
            book = loan_info['book']
            print(f"Title: {book['title']}, Author: {book['author']}, Loaned by: {loan_info['loaned_by']}")

if __name__ == "__main__":
    global_library = [
        {'title': 'Book_1', 'author': 'Author_1', 'stock': 3},
        {'title': 'Book_2', 'author': 'Author_2', 'stock': 2},
        {'title': 'Book_3', 'author': 'Author_3', 'stock': 1}
    ]

    user_manager = User(None)
    logged_in = False

    while True:
        if logged_in == False:
            print("1. Sign up")
            print("2. Sign in")
        if logged_in:
            print("3. Loan a book")
            print("4. Return a book")
            print("5. Display user's loans")
        print("6. Exit")

        choice = input("Enter your choice (1/2/3/4/5/6): ")

        if choice == '1':
            user_manager.username = user_manager.sign_up()
        elif choice == '2':
            username = user_manager.sign_in(global_library)
            if username:
                user_manager.username = username
                logged_in = True
        elif logged_in:
            if choice == '3':
                title = input("Enter the title of the book to loan: ")
                author = input("Enter the author of the book to loan: ")
                user_manager.loan_out(title, author)
            elif choice == '4':
                title = input("Enter the title of the book to return: ")
                author = input("Enter the author of the book to return: ")
                user_manager.return_in(title, author)
            elif choice == '5':
                user_manager.display_loans()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose 1, 2, 3, 4, 5, or 6.")
