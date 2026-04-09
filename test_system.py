from models import Book, BookBST, BorrowQueue
from services import BookService, UserService, BorrowService

class TestSystem:
    def __init__(self):
        self.book_bst = BookBST()
        self.borrow_queue = BorrowQueue()
        self.book_service = BookService(self.book_bst)
        self.user_service = UserService()
        self.borrow_service = BorrowService(self.book_service, self.user_service, self.borrow_queue)
        self.user_service.register_user("admin", "admin123", "admin")
    
    def test_add_book(self):
        print("=== Test: Add Books ===")
        book1 = Book("9787115588888", "Python Programming", "Zhang San", "2024-01-01", 2)
        success, message = self.book_service.add_book(book1)
        print(f"Add Book 1: {message}")
        
        book2 = Book("9787115588889", "Java Programming", "Li Si", "2024-02-01", 3)
        success, message = self.book_service.add_book(book2)
        print(f"Add Book 2: {message}")
    
    def test_search_book(self):
        print("\n=== Test: Search Books ===")
        # Search by ISBN
        results = self.book_service.search_book("isbn", "9787115588888")
        print("Search by ISBN:")
        for book in results:
            print(book)
        
        # Search by title
        results = self.book_service.search_book("title", "Programming")
        print("\nSearch by Title:")
        for book in results:
            print(book)
        
        # Search by author
        results = self.book_service.search_book("author", "Zhang")
        print("\nSearch by Author:")
        for book in results:
            print(book)
    
    def test_user_operations(self):
        print("\n=== Test: User Operations ===")
        # Register users
        success, result = self.user_service.register_user("user1", "123456")
        print(f"Register User 1: {result if not success else 'Success'}")
        
        success, result = self.user_service.register_user("user2", "123456")
        print(f"Register User 2: {result if not success else 'Success'}")
        
        # Login users
        success, user1 = self.user_service.login_user("user1", "123456")
        print(f"Login User 1: {'Success' if success else 'Failed'}")
        
        success, user2 = self.user_service.login_user("user2", "123456")
        print(f"Login User 2: {'Success' if success else 'Failed'}")
        
        return user1, user2
    
    def test_borrow_return(self, user1, user2):
        print("\n=== Test: Borrow & Return Books ===")
        # User 1 borrows a book
        success, message = self.borrow_service.borrow_book(user1, "9787115588888")
        print(f"User 1 Borrow: {message}")
        
        # User 2 borrows (only 1 stock left)
        success, message = self.borrow_service.borrow_book(user2, "9787115588888")
        print(f"User 2 Borrow: {message}")
        
        # View user 1 borrowed books
        borrowed = user1.check_borrowed()
        print("\nUser 1 Borrowed Books:")
        for book in borrowed:
            print(book)
        
        # User 1 returns book
        success, message = self.borrow_service.return_book(user1, "9787115588888")
        print(f"\nUser 1 Return: {message}")
        
        # View user 2 borrowed books
        borrowed = user2.check_borrowed()
        print("\nUser 2 Borrowed Books:")
        for book in borrowed:
            print(book)
    
    def test_queue(self, user1, user2):
        print("\n=== Test: Queue Functionality ===")
        # Borrow all stock first
        for i in range(3):
            success, message = self.borrow_service.borrow_book(user1, "9787115588889")
            print(f"User 1 Borrow Attempt {i+1}: {message}")
        
        # User 2 tries to borrow (should enter queue)
        success, message = self.borrow_service.borrow_book(user2, "9787115588889")
        print(f"User 2 Borrow: {message}")
        
        # View queue
        queue = self.borrow_service.show_borrow_queue()
        print("\nQueue Status:")
        for item in queue:
            print(item)
        
        # User 1 returns book
        success, message = self.borrow_service.return_book(user1, "9787115588889")
        print(f"\nUser 1 Return: {message}")
        
        # Check if user 2 automatically borrowed the book
        borrowed = user2.check_borrowed()
        print("\nUser 2 Borrowed Books:")
        for book in borrowed:
            print(book)
    
    def run_all_tests(self):
        self.test_add_book()
        self.test_search_book()
        user1, user2 = self.test_user_operations()
        self.test_borrow_return(user1, user2)
        self.test_queue(user1, user2)
        print("\n=== All Tests Completed ===")

if __name__ == "__main__":
    test = TestSystem()
    test.run_all_tests()
