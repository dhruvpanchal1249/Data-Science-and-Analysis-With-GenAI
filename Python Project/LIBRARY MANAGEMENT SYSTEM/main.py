import json 
import string
import random
from pathlib import Path
from datetime import datetime

class Library:
    database = "library.json"
    data = {"books": [], "members": []}

    # Load database at class loading time
    if Path(database).exists():
        with open(database, "r") as f:
            content = f.read().strip()
            if content:
                data = json.loads(content)
                # Ensure all books copies are integers
                for b in data.get("books", []):
                    try:
                        b["total_copies"] = int(b.get("total_copies", 0))
                    except (ValueError, TypeError):
                        b["total_copies"] = 0
                    try:
                        b["available_copies"] = int(b.get("available_copies", 0))
                    except (ValueError, TypeError):
                        b["available_copies"] = 0
    else:
        with open(database, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def gen_id(Prefix="B"):
        random_id = ""
        for _ in range(5):
            random_id += random.choice(string.ascii_uppercase + string.digits)
        return Prefix + "-" + random_id
    
    @classmethod    
    def save_data(cls):
        with open(cls.database, "w") as f:
            json.dump(cls.data, f, indent=4, default=str)

    # Add book function
    def add_book(self):
        title = input("Enter book title: ").strip()
        author = input("Enter book author: ").strip()
        copies_input = input("Enter number of copies: ").strip()
        try:
            copies = int(copies_input)
        except ValueError:
            print("Invalid input for copies. Defaulting to 1.")
            copies = 1

        book = {
            "id": Library.gen_id(),
            "title": title,
            "author": author,
            "total_copies": copies,
            "available_copies": copies,
            "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        Library.data["books"].append(book)
        Library.save_data()
        print(f"Book '{title}' added successfully with ID: {book['id']}")

    # List books function
    def list_books(self):
        if not Library.data["books"]:
            print("No books available")
            return
        
        print("-" * 90)
        print(f"{'Book ID':10} | {'Title':25} | {'Author':20} | {'Total':5} | {'Available':9} | {'Added On':19}")
        print("-" * 90)
        for b in Library.data["books"]:
            title = b.get('title', '')
            author = b.get('author', '')
            title_disp = title[:23] + ".." if len(title) > 25 else title
            author_disp = author[:18] + ".." if len(author) > 20 else author
            
            try:
                tot = int(b.get('total_copies', 0))
            except (ValueError, TypeError):
                tot = 0
            try:
                avail = int(b.get('available_copies', 0))
            except (ValueError, TypeError):
                avail = 0
                
            print(f"{b.get('id', ''):10} | {title_disp:25} | {author_disp:20} | {str(tot):<5} | {str(avail):<9} | {b.get('added_on', ''):19}")
        print("-" * 90)

    # Search book function
    def search_book(self):
        query = input("Enter Book Title, Author, or ID to search: ").strip().lower()
        if not query:
            print("Search query cannot be empty")
            return
        
        matches = []
        for b in Library.data["books"]:
            if (query in b.get("id", "").lower() or 
                query in b.get("title", "").lower() or 
                query in b.get("author", "").lower()):
                matches.append(b)
                
        if not matches:
            print("No matching books found")
            return
            
        print(f"\nFound {len(matches)} matching book(s):")
        print("-" * 90)
        print(f"{'Book ID':10} | {'Title':25} | {'Author':20} | {'Total':5} | {'Available':9} | {'Added On':19}")
        print("-" * 90)
        for b in matches:
            title = b.get('title', '')
            author = b.get('author', '')
            title_disp = title[:23] + ".." if len(title) > 25 else title
            author_disp = author[:18] + ".." if len(author) > 20 else author
            
            try:
                tot = int(b.get('total_copies', 0))
            except (ValueError, TypeError):
                tot = 0
            try:
                avail = int(b.get('available_copies', 0))
            except (ValueError, TypeError):
                avail = 0
                
            print(f"{b.get('id', ''):10} | {title_disp:25} | {author_disp:20} | {str(tot):<5} | {str(avail):<9} | {b.get('added_on', ''):19}")
        print("-" * 90)

    # Add member function
    def add_member(self):
        name = input("Enter member name: ").strip()
        email = input("Enter email ID: ").strip()
        member = {
            "id": Library.gen_id("M"),
            "name": name,
            "email": email,
            "borrowed_books": []
        }
        Library.data["members"].append(member)
        Library.save_data()
        print(f"Member '{name}' added successfully with ID: {member['id']}")

    # List member function
    def list_member(self):
        if not Library.data["members"]:
            print("No members available")
            return
        
        print("-" * 75)
        print(f"{'Member ID':12} | {'Name':20} | {'Email':30}")
        print("-" * 75)
        for m in Library.data["members"]:
            print(f"{m.get('id', ''):12} | {m.get('name', ''):20} | {m.get('email', ''):30}")
            borrowed = m.get("borrowed_books", [])
            if borrowed:
                titles = ", ".join([b["title"] for b in borrowed])
                print(f"   -> Borrowed Books: {titles}")
            else:
                print("   -> Borrowed Books: None")
            print("-" * 75)

    # Borrow book function
    def borrow(self):
        member_id = input("Enter member ID: ").strip()
        members = [m for m in Library.data["members"] if m["id"] == member_id]
        if not members:
            print("Member not found")
            return
        member = members[0]
        
        book_id = input("Enter book ID: ").strip()
        books = [b for b in Library.data["books"] if b["id"] == book_id]
        if not books:
            print("Book not found")
            return
        book = books[0]
        
        try:
            available_copies = int(book.get('available_copies', 0))
        except (ValueError, TypeError):
            available_copies = 0

        if available_copies <= 0:
            print("No copies available")
            return

        borrow_entry = {
            "book_id": book['id'],
            "borrow_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "title": book['title'],
        }
        
        # Initialize borrowed_books if missing
        if "borrowed_books" not in member:
            member["borrowed_books"] = []
            
        member['borrowed_books'].append(borrow_entry)
        book['available_copies'] = available_copies - 1
        Library.save_data()
        print("Book borrowed successfully")

    # Return book function
    def return_book(self):
        member_id = input("Enter member ID: ").strip()
        members = [m for m in Library.data["members"] if m["id"] == member_id]
        if not members:
            print("Member not found")
            return
        member = members[0]
        
        borrowed_books = member.get("borrowed_books", [])
        if not borrowed_books:
            print("No books borrowed by this member")
            return
        
        print("Borrowed books:")
        for i, b in enumerate(borrowed_books, start=1):
            print(f"{i}. {b['title']} (Borrowed date: {b.get('borrow_date', 'N/A')})")

        try:
            choice = int(input("Enter the Choice No to return: "))
            if choice < 1 or choice > len(borrowed_books):
                print("Invalid Choice")
                return
            selected = borrowed_books.pop(choice - 1)
        except Exception:
            print("Invalid input")
            return

        # Return the copy to the book's availability
        books = [b for b in Library.data["books"] if b["id"] == selected["book_id"]]
        if books:
            book = books[0]
            try:
                available_copies = int(book.get("available_copies", 0))
            except (ValueError, TypeError):
                available_copies = 0
            book["available_copies"] = available_copies + 1
        
        Library.save_data()
        print(f"Book '{selected['title']}' returned successfully")


def main():
    hello = Library()

    while True:
        print("\n" + "="*50)
        print("Library Management System")
        print("="*50)
        print("1. Add Book")
        print("2. List Books")
        print("3. Add Member")
        print("4. List Members")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. Search Book")
        print("8. Exit")
        print("-"*50)
        
        choice = input("Enter your choice (1-8): ").strip()
        print("-"*50)
        
        if choice == "1":
            hello.add_book()
        elif choice == "2":
            hello.list_books()
        elif choice == "3":
            hello.add_member()
        elif choice == "4":
            hello.list_member()
        elif choice == "5":
            hello.borrow()
        elif choice == "6":
            hello.return_book()
        elif choice == "7":
            hello.search_book()
        elif choice == "8":
            print("Exiting Library Management System. Goodbye!")
            break
        else:
            print("Invalid Choice, please select a number from 1 to 8")

if __name__ == "__main__":
    main()