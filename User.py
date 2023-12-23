import os 

class Book:
    def __init__(self,isbn,title,author,section,stock):
        self.isbn = int(isbn)
        self.title = str(title)
        self.author = str(author)
        self.section = int(section)
        self.stock = int(stock)

class User:

    def __init__(self, username):
        self.username = username

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
            file.write(f"\n{username},{passwordHash}")
        return "Signup successful!"

    def sign_in(self, library, username, password):
        passwordHash = self.myHash(password)

        with open("users.txt", "r") as file:
            for line in file:
                existing_username, existing_password = line.strip().split(',')
                if existing_username == username and existing_password.strip() == passwordHash:
                    self.library = library.copy() 
                    return username
        print("Wrong username or password.\nPlease try again.")
        return None

    def loan_out(self, book:Book):

        #Checks for the book in the users file of loans
        def create_file_if_not_exist(folder_path, file_name):
            file_path = os.path.join(folder_path, file_name)
            if not os.path.exists(file_path):
                # Create the file if it doesn't exist
                with open(file_path, 'w'):
                    pass  # Empty context manager to create the file

        create_file_if_not_exist("UserFiles", f"{self.username}.txt") 

        with open(f"UserFiles/{self.username}.txt", "r", encoding="utf-8") as file:
            for line in file:
                data = line.strip().split(",")
                if data == [str(book.isbn), book.title, book.author, str(book.section)]:
                    return None        
                    
        loan_info = f"Book '{book.title}' by '{book.author}' loaned out successfully by '{self.username}'\n"
        with open("MovesLog.txt", "a", encoding="utf-8") as file:
            file.write(loan_info)
        
        with open(f"UserFiles/{self.username}.txt", "a", encoding="utf-8") as file:
            file.write(f"{book.isbn},{book.title},{book.author},{book.section}\n")

        return "Done"
        
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

