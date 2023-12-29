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

    def sign_in(self, username, password):
        passwordHash = self.myHash(password)

        with open("users.txt", "r") as file:
            for line in file:
                existing_username, existing_password = line.strip().split(',')
                if existing_username == username and existing_password.strip() == passwordHash:
                    return username
        return None

    #Checks for the book in the users file of loans
    def create_file_if_not_exist(self, folder_path, file_name):
        file_path = os.path.join(folder_path, file_name)
        if not os.path.exists(file_path):
            # Create the file if it doesn't exist
            with open(file_path, 'w'):
                pass  # Empty context manager to create the file
    
    def delete_line_from_file(self, file_path, line_to_delete):
        # Read all lines from the file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Remove the specified line
        lines = [line for line in lines if line.strip() != line_to_delete.strip()]

        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.writelines(lines)

    def loan_out(self, book:Book): 
        self.create_file_if_not_exist("UserFiles", f"{self.username}.txt")
        #If the book is already in the user's txt it's not loaned out
        with open(f"UserFiles/{self.username}.txt", "r", encoding="utf-8") as file:
            for line in file:
                data = line.strip().split("\t\t")
                if data:
                    if data == [str(book.isbn), book.title, book.author, str(book.section)]:
                        return None
                    
        loan_info = f"'{book.title} by {book.author}' loaned out by '{self.username}'\n"
        
        #Logs the loan info into a seperate file
        with open("MovesLog.txt", "a", encoding="utf-8") as file:
            file.write(loan_info)

        #Add the book's info into the user's file
        with open(f"UserFiles/{self.username}.txt", "a", encoding="utf-8") as file:
            file.write(f"{book.isbn}\t\t{book.title}\t\t{book.author}\t\t{book.section}\n")

        return "Done"
        
    def return_in(self, book:Book):
        deleted = False
        self.create_file_if_not_exist("UserFiles", f"{self.username}.txt")
        with open(f"UserFiles/{self.username}.txt", "r", encoding="utf-8") as file:
            for line in file:
                data = line.strip().split("\t\t")
                if data:
                    if data == [str(book.isbn), book.title, book.author, str(book.section)]:
                        self.delete_line_from_file(f"UserFiles/{self.username}.txt",line)
                        deleted = True
        if deleted:
            #Captures the return only when the book is loaned out by the user
            returnInfo = f"'{book.title} by {book.author}' returned in by '{self.username}'\n"
            with open("MovesLog.txt", "a", encoding="utf-8") as file:
                file.write(returnInfo)
            return True
        else:
            return None


