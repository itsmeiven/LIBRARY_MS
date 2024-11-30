import datetime
import csv
import os

class LibrarySystem:
    def __init__(self):
        # Predefined books in the library (always available even if no CSV file exists)
        self.default_books = {
            "B001": {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "copies": 5, "publish_year": 1997},
            "B002": {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "copies": 3, "publish_year": 1925},
            "B003": {"title": "1984", "author": "George Orwell", "copies": 4, "publish_year": 1949},
        }
        
        self.books = {}
        self.users = {}
        self.history = []
        self.librarian_password = "library"
        self.load_data()  # Load data from CSV or use default data if no CSV exists
        
    # Save data to CSV files
    def save_data(self):
        # Save books data
        with open("books.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["book_id", "title", "author", "copies", "publish_year"])
            writer.writeheader()
            for book_id, details in self.books.items():
                writer.writerow({"book_id": book_id, **details})
        
        # Save users data
        with open("users.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["username", "section", "borrowed_books"])
            writer.writeheader()
            for username, details in self.users.items():
                writer.writerow({"username": username, "section": details["section"], "borrowed_books": str(details["borrowed_books"])})

        # Save history data
        with open("history.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["username", "book_id", "quantity", "borrow_date", "return_date", "remarks"])
            writer.writeheader()
            for record in self.history:
                writer.writerow(record)

        print("Data saved successfully!")

    # Load data from CSV files
    def load_data(self):
        # Start with the default books
        self.books = self.default_books.copy()

        if os.path.exists("books.csv"):
            with open("books.csv", "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.books[row["book_id"]] = {
                        "title": row["title"],
                        "author": row["author"],
                        "copies": int(row["copies"]),
                        "publish_year": int(row["publish_year"]),
                    }
            print("Books data loaded successfully!")

        if os.path.exists("users.csv"):
            with open("users.csv", "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    borrowed_books = eval(row["borrowed_books"])  # Convert string back to list of dicts
                    self.users[row["username"]] = {"section": row["section"], "borrowed_books": borrowed_books}
            print("Users data loaded successfully!")

        if os.path.exists("history.csv"):
            with open("history.csv", "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.history.append(row)
            print("History data loaded successfully!")
        else:
            print("No saved data found, starting with default books.")

    # Add User
    def add_user(self, username, section):
        if username not in self.users:
            self.users[username] = {"section": section, "borrowed_books": []}
            print(f"User '{username}' from Section '{section}' added successfully!")
            self.save_data()  # Save data after changes
        else:
            print("User already exists.")

    # Add Book
    def add_book(self, book_id, title, author, copies, publish_year):
        if book_id not in self.books:
            self.books[book_id] = {
                "title": title,
                "author": author,
                "copies": copies,
                "publish_year": publish_year,
            }
            print(f"Book '{title}' added successfully!")
            self.save_data()  # Save data after changes
        else:
            print("Book already exists.")

    # Borrow Book
    def borrow_book(self, username, book_id, quantity, return_date):
        if username not in self.users:
            print("User not found. Please add the user first.")
            return

        if book_id in self.books and self.books[book_id]["copies"] >= quantity:
            self.books[book_id]["copies"] -= quantity
            borrow_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.users[username]["borrowed_books"].append({
                "book_id": book_id,
                "quantity": quantity,
                "borrow_date": borrow_date,
                "return_date": return_date,
                "remarks": "Borrowed",
            })
            self.history.append({
                "username": username,
                "book_id": book_id,
                "quantity": quantity,
                "borrow_date": borrow_date,
                "return_date": return_date,
                "remarks": "Borrowed",
            })
            print(f"Book '{self.books[book_id]['title']}' borrowed successfully!")
            self.save_data()  # Save data after changes
        else:
            print("Not enough copies available or book does not exist.")

    # Return Book
    def return_book(self, username, book_id, quantity):
        if username in self.users:
            borrowed_books = self.users[username]["borrowed_books"]
            for record in borrowed_books:
                if record["book_id"] == book_id and record["quantity"] == quantity:
                    borrowed_books.remove(record)  # Remove from user's borrowed list
                    self.books[book_id]["copies"] += quantity  # Return copies
                    return_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    overdue = self.check_overdue(record["return_date"])
                    remarks = "Overdue" if overdue else "Returned"
                    self.history.append({
                        "username": username,
                        "book_id": book_id,
                        "quantity": quantity,
                        "return_date": return_date,
                        "remarks": remarks,
                    })
                    print(f"Book '{self.books[book_id]['title']}' returned successfully!")
                    self.save_data()  # Save data after changes
                    return
            print("This book was not borrowed by the user or quantity mismatched.")
        else:
            print("User not found.")

    # Check Overdue
    def check_overdue(self, return_date):
        current_date = datetime.datetime.now()
        return_date_obj = datetime.datetime.strptime(return_date, "%Y-%m-%d %H:%M:%S")
        return current_date > return_date_obj

    # View History (Librarian only)
    def view_history(self, password):
        if password == self.librarian_password:
            print("\n--- Borrowing/Returning History ---")
            for record in self.history:
                print(record)
        else:
            print("Incorrect password.")

    # Display Books
    def display_books(self):
        print("\n--- Library Books ---")
        for book_id, details in self.books.items():
            print(f"ID: {book_id}, Title: {details['title']}, Author: {details['author']}, Copies: {details['copies']}, Year: {details['publish_year']}")

    # Show Menu for Users
    def show_user_menu(self):
        print("\n--- User Menu ---")
        print("1. Display All Books")
        print("2. Borrow Book")
        print("3. Return Book")
        print("4. Exit")

    # Show Menu for Librarians
    def show_librarian_menu(self):
        print("\n--- Librarian Menu ---")
        print("1. Display All Books")
        print("2. Add Book")
        print("3. Add User")
        print("4. View Borrowing/Returning History")
        print("5. Exit")

    # Main Program Logic
    def start(self):
        while True:
            print("\n--- WELCOME TO LIBRARY MANAGEMENT SYSTEM ---")
            print("[1] Librarian")
            print("[2] Student")
            user_type = input("Choose your role (1 or 2): ")

            if user_type == "1":
                while True:
                    password = input("Enter librarian password or type 'exit' to quit: ")
                    if password == "exit":
                        print("Exiting Librarian Login...")
                        break
                    elif password == self.librarian_password:
                        while True:
                            self.show_librarian_menu()
                            choice = input("Choose an option: ")

                            if choice == "1":
                                self.display_books()

                            elif choice == "2":
                                book_id = input("Enter book ID: ")
                                title = input("Enter book title: ")
                                author = input("Enter author: ")
                                copies = int(input("Enter number of copies: "))
                                publish_year = int(input("Enter publish year: "))
                                self.add_book(book_id, title, author, copies, publish_year)

                            elif choice == "3":
                                username = input("Enter username: ")
                                section = input("Enter section: ")
                                self.add_user(username, section)

                            elif choice == "4":
                                self.view_history(password)

                            elif choice == "5":
                                print("Exiting Librarian Menu...")
                                break

                            else:
                                print("Invalid option. Please try again.")
                        break
                    else:
                        print("Incorrect password. Please try again.")
                        continue

            elif user_type == "2":
                while True:
                    self.show_user_menu()
                    choice = input("Choose an option: ")

                    if choice == "1":
                        self.display_books()

                    elif choice == "2":
                        username = input("Enter your username: ")
                        if username not in self.users:
                            print(f"User '{username}' not found. Please register first.")
                            register = input("Do you want to register now? (y/n): ")
                            if register.lower() == 'y':
                                section = input("Enter your section: ")
                                self.add_user(username, section)

                        while True:
                            book_id = input("Enter book ID to borrow: ")
                            quantity = 1  # Default to borrowing 1 copy

                            while True:
                                suggested_date = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
                                return_date_input = input(f"Enter return date (YYYY-MM-DD) [e.g., {suggested_date}]: ")
                                try:
                                    return_date = datetime.datetime.strptime(return_date_input, "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S")
                                    if datetime.datetime.strptime(return_date, "%Y-%m-%d %H:%M:%S") < datetime.datetime.now():
                                        print("Error: Return date cannot be earlier than the current date.")
                                        continue
                                    self.borrow_book(username, book_id, quantity, return_date)
                                    break
                                except ValueError:
                                    print("Invalid date format. Please use YYYY-MM-DD.")
                                    continue

                            more_books = input("Do you want to borrow more books? (y/n): ")
                            if more_books.lower() != 'y':
                                break

                    elif choice == "3":
                        username = input("Enter your username: ")
                        book_id = input("Enter book ID to return: ")
                        quantity = int(input("Enter number of books to return: "))
                        self.return_book(username, book_id, quantity)

                    elif choice == "4":
                        print("Exiting Student Menu...")
                        break

                    else:
                        print("Invalid option. Please try again.")

            else:
                print("Invalid option. Please choose either '1' for Librarian or '2' for Student.")


# Run the system
library_system = LibrarySystem()
library_system.start()