from models import Book, User, AdminUser, BookBST, BorrowQueue

class BookService:
    def __init__(self, book_bst):
        self.book_bst = book_bst
    
    def add_book(self, book):
        if not book.validate_isbn():
            return False, "Invalid ISBN format"
        existing_book = self.book_bst.search_book_by_isbn(book.isbn)
        if existing_book:
            return False, "ISBN already exists"
        success = self.book_bst.insert_book(book)
        if success:
            return True, "Book added successfully"
        return False, "Failed to add book"
    
    def delete_book(self, isbn):
        book = self.book_bst.search_book_by_isbn(isbn)
        if not book:
            return False, "Book not found"
        if book.status == "Borrowed":
            return False, "Book is currently borrowed and cannot be deleted"
        self.book_bst.delete_book(isbn)
        return True, "Book deleted successfully"
    
    def update_book(self, isbn, new_info):
        book = self.book_bst.search_book_by_isbn(isbn)
        if not book:
            return False, "Book not found"
        success = self.book_bst.update_book(isbn, new_info)
        if success:
            return True, "Book updated successfully"
        return False, "Failed to update book"
    
    def search_book(self, by, keyword):
        if by == "isbn":
            book = self.book_bst.search_book_by_isbn(keyword)
            return [book] if book else []
        elif by == "title":
            return self.book_bst.search_book_by_title(keyword)
        elif by == "author":
            return self.book_bst.search_book_by_author(keyword)
        return []
    
    def list_all_books(self):
        return self.book_bst.inorder_traversal()

class UserService:
    def __init__(self):
        self._users = {}
        self._user_id_counter = 1
    
    def register_user(self, username, password, role="normal"):
        for user in self._users.values():
            if user.username == username:
                return False, "Username already exists"
        user_id = f"U{self._user_id_counter:03d}"
        self._user_id_counter += 1
        if role == "admin":
            user = AdminUser(user_id, username, password)
        else:
            user = User(user_id, username, password, role)
        self._users[user_id] = user
        return True, user
    
    def login_user(self, username, password):
        for user in self._users.values():
            if user.username == username and user.login(password):
                return True, user
        return False, "Incorrect username or password"
    
    def check_permission(self, user, required_role):
        return user.check_permission(required_role)
    
    def get_user_by_id(self, user_id):
        return self._users.get(user_id)

class BorrowService:
    def __init__(self, book_service, user_service, borrow_queue):
        self.book_service = book_service
        self.user_service = user_service
        self.borrow_queue = borrow_queue
    
    def borrow_book(self, user, isbn):
        book = self.book_service.book_bst.search_book_by_isbn(isbn)
        if not book:
            return False, "Book not found"
        success, message = user.borrow_book(book)
        if not success:
            return False, message
        if book.stock > 0:
            book.change_stock(-1)
            return True, "Borrow successful"
        else:
            self.borrow_queue.enqueue(user.user_id, isbn)
            position = self.borrow_queue.get_user_position(user.user_id, isbn)
            return True, f"No stock available. You have been added to the queue. Your position: {position}"
    
    def return_book(self, user, isbn):
        book = self.book_service.book_bst.search_book_by_isbn(isbn)
        if not book:
            return False, "Book not found"
        success, message = user.return_book(book)
        if not success:
            return False, message
        book.change_stock(1)
        queued_item = self.borrow_queue.dequeue(isbn)
        if queued_item:
            queued_user = self.user_service.get_user_by_id(queued_item['user_id'])
            if queued_user:
                queued_user.borrow_book(book)
                book.change_stock(-1)
                return True, f"Return successful. Book automatically borrowed by queued user {queued_user.username}"
        return True, "Return successful"
    
    def process_queue(self, isbn):
        queued_item = self.borrow_queue.dequeue(isbn)
        if not queued_item:
            return False, "No queue records for this book"
        book = self.book_service.book_bst.search_book_by_isbn(isbn)
        if not book or book.stock <= 0:
            return False, "No stock available"
        user = self.user_service.get_user_by_id(queued_item['user_id'])
        if not user:
            return False, "User not found"
        success, message = user.borrow_book(book)
        if success:
            book.change_stock(-1)
            return True, f"Borrow processed for user {user.username}"
        return False, message
    
    def show_borrow_queue(self):
        return self.borrow_queue.show_queue()
