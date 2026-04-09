from abc import ABC, abstractmethod
from datetime import datetime

class BaseUser(ABC):
    def __init__(self, user_id, username, role):
        self._user_id = user_id
        self._username = username
        self._role = role
    
    @abstractmethod
    def borrow_book(self, book):
        pass
    
    @abstractmethod
    def return_book(self, book):
        pass
    
    @abstractmethod
    def check_permission(self, required_role):
        pass

class BaseDataStructure(ABC):
    @abstractmethod
    def add(self, item):
        pass
    
    @abstractmethod
    def remove(self, item):
        pass
    
    @abstractmethod
    def search(self, key):
        pass

class Book:
    def __init__(self, isbn, title, author, publish_date, stock):
        self._isbn = isbn
        self._title = title
        self._author = author
        self._publish_date = publish_date
        self._stock = stock
        self._status = "Available" if stock > 0 else "Borrowed"
    
    def __str__(self):
        return (
            f"ISBN: {self._isbn}, Title: {self._title}, Author: {self._author}, "
            f"Publish Date: {self._publish_date}, Stock: {self._stock}, Status: {self._status}"
        )
    
    def __eq__(self, other):
        if isinstance(other, Book):
            return self._isbn == other._isbn
        return False
    
    def validate_isbn(self):
        return len(self._isbn) == 13
    
    def update_info(self, new_title=None, new_author=None, new_publish_date=None):
        if new_title:
            self._title = new_title
        if new_author:
            self._author = new_author
        if new_publish_date:
            self._publish_date = new_publish_date
    
    def change_stock(self, num):
        self._stock += num
        self._status = "Available" if self._stock > 0 else "Borrowed"
    
    @property
    def isbn(self):
        return self._isbn
    
    @property
    def title(self):
        return self._title
    
    @property
    def author(self):
        return self._author
    
    @property
    def stock(self):
        return self._stock
    
    @property
    def status(self):
        return self._status

class User(BaseUser):
    def __init__(self, user_id, username, password, role="normal"):
        super().__init__(user_id, username, role)
        self._password = password
        self._borrowed_books = []
        self._max_borrow = 5
    
    def borrow_book(self, book):
        if len(self._borrowed_books) >= self._max_borrow:
            return False, "Reached maximum borrowing limit"
        if book.isbn in [b.isbn for b in self._borrowed_books]:
            return False, "You have already borrowed this book"
        self._borrowed_books.append(book)
        return True, "Borrow successful"
    
    def return_book(self, book):
        for b in self._borrowed_books:
            if b.isbn == book.isbn:
                self._borrowed_books.remove(b)
                return True, "Return successful"
        return False, "You have not borrowed this book"
    
    def check_permission(self, required_role):
        return self._role == required_role
    
    def register(self):
        return "Registration successful"
    
    def login(self, password):
        return self._password == password
    
    def check_borrowed(self):
        return self._borrowed_books
    
    @property
    def user_id(self):
        return self._user_id
    
    @property
    def username(self):
        return self._username
    
    @property
    def role(self):
        return self._role

class AdminUser(User):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password, "admin")
        self._max_borrow = float('inf')
    
    def check_permission(self, required_role):
        return True
    
    def borrow_book(self, book):
        if book.isbn in [b.isbn for b in self._borrowed_books]:
            return False, "You have already borrowed this book"
        self._borrowed_books.append(book)
        return True, "Borrow successful"
    
    def manage_user(self, user, new_role):
        user._role = new_role
        return "User role updated successfully"
    
    def manage_book(self, book, new_info):
        book.update_info(**new_info)
        return "Book information updated successfully"

class BinaryTreeNode:
    def __init__(self, book):
        self.book = book
        self.left = None
        self.right = None
    
    def compare_isbn(self, target_isbn):
        if self.book.isbn < target_isbn:
            return -1
        elif self.book.isbn > target_isbn:
            return 1
        else:
            return 0

class BookBST(BaseDataStructure):
    def __init__(self):
        self.root = None
    
    def add(self, book):
        self.insert_book(book)
    
    def remove(self, isbn):
        self.delete_book(isbn)
    
    def search(self, key):
        return self.search_book_by_isbn(key)
    
    def insert_book(self, book):
        if not self.root:
            self.root = BinaryTreeNode(book)
            return True
        return self._insert_recursive(self.root, book)
    
    def _insert_recursive(self, node, book):
        if book.isbn < node.book.isbn:
            if not node.left:
                node.left = BinaryTreeNode(book)
                return True
            return self._insert_recursive(node.left, book)
        elif book.isbn > node.book.isbn:
            if not node.right:
                node.right = BinaryTreeNode(book)
                return True
            return self._insert_recursive(node.right, book)
        else:
            return False
    
    def delete_book(self, isbn):
        self.root = self._delete_recursive(self.root, isbn)
    
    def _delete_recursive(self, node, isbn):
        if not node:
            return None
        if isbn < node.book.isbn:
            node.left = self._delete_recursive(node.left, isbn)
        elif isbn > node.book.isbn:
            node.right = self._delete_recursive(node.right, isbn)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            min_node = self._find_min(node.right)
            node.book = min_node.book
            node.right = self._delete_recursive(node.right, min_node.book.isbn)
        return node
    
    def _find_min(self, node):
        while node.left:
            node = node.left
        return node
    
    def search_book_by_isbn(self, isbn):
        return self._search_recursive(self.root, isbn)
    
    def _search_recursive(self, node, isbn):
        if not node:
            return None
        if isbn == node.book.isbn:
            return node.book
        elif isbn < node.book.isbn:
            return self._search_recursive(node.left, isbn)
        else:
            return self._search_recursive(node.right, isbn)
    
    def search_book_by_title(self, keyword):
        results = []
        self._search_title_recursive(self.root, keyword, results)
        return results
    
    def _search_title_recursive(self, node, keyword, results):
        if node:
            self._search_title_recursive(node.left, keyword, results)
            if keyword.lower() in node.book.title.lower():
                results.append(node.book)
            self._search_title_recursive(node.right, keyword, results)
    
    def search_book_by_author(self, keyword):
        results = []
        self._search_author_recursive(self.root, keyword, results)
        return results
    
    def _search_author_recursive(self, node, keyword, results):
        if node:
            self._search_author_recursive(node.left, keyword, results)
            if keyword.lower() in node.book.author.lower():
                results.append(node.book)
            self._search_author_recursive(node.right, keyword, results)
    
    def update_book(self, isbn, new_info):
        book = self.search_book_by_isbn(isbn)
        if book:
            book.update_info(**new_info)
            return True
        return False
    
    def inorder_traversal(self):
        books = []
        self._inorder_recursive(self.root, books)
        return books
    
    def _inorder_recursive(self, node, books):
        if node:
            self._inorder_recursive(node.left, books)
            books.append(node.book)
            self._inorder_recursive(node.right, books)

class BorrowQueue(BaseDataStructure):
    def __init__(self):
        self._queue = []
    
    def add(self, item):
        self.enqueue(item['user_id'], item['isbn'])
    
    def remove(self, item):
        self.dequeue(item['isbn'])
    
    def search(self, key):
        return self.get_user_position(key['user_id'], key['isbn'])
    
    def enqueue(self, user_id, isbn):
        queue_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        self._queue.append({"user_id": user_id, "isbn": isbn, "queue_time": queue_time})
    
    def dequeue(self, isbn):
        for i, item in enumerate(self._queue):
            if item['isbn'] == isbn:
                return self._queue.pop(i)
        return None
    
    def is_empty(self):
        return len(self._queue) == 0
    
    def show_queue(self, isbn=None):
        if isbn:
            return [item for item in self._queue if item['isbn'] == isbn]
        return self._queue
    
    def get_user_position(self, user_id, isbn):
        for i, item in enumerate(self._queue):
            if item['user_id'] == user_id and item['isbn'] == isbn:
                return i + 1
        return -1
