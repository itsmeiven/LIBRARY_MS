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

 