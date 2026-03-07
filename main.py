from models import BookBST, BorrowQueue
from services import BookService, UserService, BorrowService

class LibraryManagementSystem:
    def __init__(self):
        self.book_bst = BookBST()
        self.borrow_queue = BorrowQueue()
        self.book_service = BookService(self.book_bst)
        self.user_service = UserService()
        self.borrow_service = BorrowService(self.book_service, self.user_service, self.borrow_queue)
        self._init_default_admin()
    
    def _init_default_admin(self):
        self.user_service.register_user("admin", "admin123", "admin")
    
    def run(self):
        while True:
            self.show_main_menu()
            choice = input("Please select an option: ")
            if choice == "1":
                self.register_user()
            elif choice == "2":
                self.login_user()
            elif choice == "3":
                print("Thank you for using the system. Goodbye!")
                break
            else:
                print("Invalid input, please try again.")
    
    def show_main_menu(self):
        print("\n===== Library Management System =====")
        print("1. User Registration")
        print("2. User Login")
        print("3. Exit")
    
    def register_user(self):
        print("\n===== User Registration =====")
        username = input("Enter username: ")
        password = input("Enter password: ")
        role = input("Enter role (normal/admin): ").lower()
        if role not in ["normal", "admin"]:
            role = "normal"
        success, result = self.user_service.register_user(username, password, role)
        if success:
            print(f"Registration successful, User ID: {result.user_id}")
        else:
            print(result)
    
    def login_user(self):
        print("\n===== User Login =====")
        for i in range(3):
            username = input("Enter username: ")
            password = input("Enter password: ")
            success, result = self.user_service.login_user(username, password)
            if success:
                print(f"Login successful, welcome {result.username}!")
                if result.role == "admin":
                    self.show_admin_menu(result)
                else:
                    self.show_user_menu(result)
                return
            else:
                print(result)
                if i < 2:
                    print(f"You have {2 - i} attempts left.")
        print("Too many failed attempts. Please try again later.")
    
    def show_admin_menu(self, user):
        while True:
            print("\n===== Admin Menu =====")
            print("1. Book Management")
            print("2. User Management")
            print("3. Borrow/Return Management")
            print("4. Logout")
            choice = input("Please select an option: ")
            if choice == "1":
                self.manage_books(user)
            elif choice == "2":
                self.manage_users(user)
            elif choice == "3":
                self.manage_borrows(user)
            elif choice == "4":
                print("Logout successful.")
                break
            else:
                print("Invalid input, please try again.")
    
    def show_user_menu(self, user):
        while True:
            print("\n===== User Menu =====")
            print("1. Search Books")
            print("2. Borrow Book")
            print("3. Return Book")
            print("4. View Borrowed Books")
            print("5. View Queue Records")
            print("6. Logout")
            choice = input("Please select an option: ")
            if choice == "1":
                self.search_books(user)
            elif choice == "2":
                self.borrow_book(user)
            elif choice == "3":
                self.return_book(user)
            elif choice == "4":
                self.view_borrowed_books(user)
            elif choice == "5":
                self.view_queue(user)
            elif choice == "6":
                print("Logout successful.")
                break
            else:
                print("Invalid input, please try again.")
    
    def manage_books(self, user):
        while True:
            print("\n===== Book Management =====")
            print("1. Add Book")
            print("2. Delete Book")
            print("3. Update Book")
            print("4. Search Book")
            print("5. View All Books")
            print("6. Back")
            choice = input("Please select an option: ")
            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.delete_book()
            elif choice == "3":
                self.update_book()
            elif choice == "4":
                self.search_books(user)
            elif choice == "5":
                self.list_all_books()
            elif choice == "6":
                break
            else:
                print("Invalid input, please try again.")
    
    def add_book(self):
        print("\n===== Add Book =====")
        isbn = input("Enter ISBN (13 digits): ")
        title = input("Enter title: ")
        author = input("Enter author: ")
        publish_date = input("Enter publish date (YYYY-MM-DD): ")
        stock = int(input("Enter stock: "))
        book = Book(isbn, title, author, publish_date, stock)
        success, message = self.book_service.add_book(book)
        print(message)
    
    def delete_book(self):
        print("\n===== Delete Book =====")
        isbn = input("Enter ISBN of the book to delete: ")
        success, message = self.book_service.delete_book(isbn)
        print(message)
    
    def update_book(self):
        print("\n===== Update Book =====")
        isbn = input("Enter ISBN of the book to update: ")
        new_title = input("Enter new title (press Enter to skip): ")
        new_author = input("Enter new author (press Enter to skip): ")
        new_publish_date = input("Enter new publish date (press Enter to skip): ")
        new_info = {}
        if new_title:
            new_info['new_title'] = new_title
        if new_author:
            new_info['new_author'] = new_author
        if new_publish_date:
            new_info['new_publish_date'] = new_publish_date
        success, message = self.book_service.update_book(isbn, new_info)
        print(message)
    
    def search_books(self, user):
        print("\n===== Search Books =====")
        print("1. Search by ISBN")
        print("2. Search by Title")
        print("3. Search by Author")
        choice = input("Select search method: ")
        if choice == "1":
            keyword = input("Enter ISBN: ")
            results = self.book_service.search_book("isbn", keyword)
        elif choice == "2":
            keyword = input("Enter title keyword: ")
            results = self.book_service.search_book("title", keyword)
        elif choice == "3":
            keyword = input("Enter author keyword: ")
            results = self.book_service.search_book("author", keyword)
        else:
            print("Invalid input.")
            return
        if results:
            print("\nSearch Results:")
            for book in results:
                print(book)
        else:
            print("No matching books found.")
    
    def list_all_books(self):
        print("\n===== All Books =====")
        books = self.book_service.list_all_books()
        if books:
            for book in books:
                print(book)
        else:
            print("No books available.")
    
    def manage_users(self, user):
        print("\n===== User Management =====")
        print("1. View All Users")
        print("2. Change User Role")
        print("3. Back")
        choice = input("Please select an option: ")
        if choice == "1":
            self.list_all_users()
        elif choice == "2":
            self.change_user_role()
        elif choice == "3":
            return
        else:
            print("Invalid input.")
    
    def list_all_users(self):
        print("\n===== All Users =====")
        for user_id, user in self.user_service._users.items():
            print(f"User ID: {user_id}, Username: {user.username}, Role: {user.role}")
    
    def change_user_role(self):
        print("\n===== Change User Role =====")
        user_id = input("Enter User ID: ")
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            print("User not found.")
            return
        new_role = input("Enter new role (normal/admin): ").lower()
        if new_role not in ["normal", "admin"]:
            print("Invalid role.")
            return
        admin = None
        for u in self.user_service._users.values():
            if u.role == "admin":
                admin = u
                break
        if admin:
            message = admin.manage_user(user, new_role)
            print(message)
        else:
            print("No admin privileges.")
    
    def manage_borrows(self, user):
        print("\n===== Borrow/Return Management =====")
        print("1. View Queue")
        print("2. Process Queue")
        print("3. Back")
        choice = input("Please select an option: ")
        if choice == "1":
            self.view_all_queue()
        elif choice == "2":
            self.process_queue()
        elif choice == "3":
            return
        else:
            print("Invalid input.")
    
    def borrow_book(self, user):
        print("\n===== Borrow Book =====")
        isbn = input("Enter ISBN of the book to borrow: ")
        success, message = self.borrow_service.borrow_book(user, isbn)
        print(message)
    
    def return_book(self, user):
        print("\n===== Return Book =====")
        isbn = input("Enter ISBN of the book to return: ")
        success, message = self.borrow_service.return_book(user, isbn)
        print(message)
    
    def view_borrowed_books(self, user):
        print("\n===== Borrowed Books =====")
        books = user.check_borrowed()
        if books:
            for book in books:
                print(book)
        else:
            print("You have no borrowed books.")
    
    def view_queue(self, user):
        print("\n===== Queue Records =====")
        queue = self.borrow_service.show_borrow_queue()
        user_queue = [item for item in queue if item['user_id'] == user.user_id]
        if user_queue:
            for item in user_queue:
                book = self.book_service.book_bst.search_book_by_isbn(item['isbn'])
                book_title = book.title if book else "Unknown Book"
                print(f"Book: {book_title}, Queue Time: {item['queue_time']}")
        else:
            print("You have no queue records.")
    
    def view_all_queue(self):
        print("\n===== All Queue Records =====")
        queue = self.borrow_service.show_borrow_queue()
        if queue:
            for item in queue:
                user = self.user_service.get_user_by_id(item['user_id'])
                user_name = user.username if user else "Unknown User"
                book = self.book_service.book_bst.search_book_by_isbn(item['isbn'])
                book_title = book.title if book else "Unknown Book"
                print(f"User: {user_name}, Book: {book_title}, Queue Time: {item['queue_time']}")
        else:
            print("No queue records.")
    
    def process_queue(self):
        print("\n===== Process Queue =====")
        isbn = input("Enter ISBN to process queue: ")
        success, message = self.borrow_service.process_queue(isbn)
        print(message)

if __name__ == "__main__":
    from models import Book
    system = LibraryManagementSystem()
    system.run()
