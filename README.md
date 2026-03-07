# Library Management System

A comprehensive library management system built with Python, featuring object-oriented design, efficient data structures, and complete user/book/borrowing management functionality.

## Project Structure
```
library_management_system/
├── main.py          # Program entry point & menu interaction
├── models.py        # Core class definitions (User, Book, BST, Queue)
├── services.py      # Business logic layer (Book/User/Borrow services)
├── utils.py         # Utility functions (validation, formatting, etc.)
└── README.md        # Project documentation
```

## Core Features

### 1. User Management
- User registration (supports `normal` and `admin` roles)
- Secure login with 3 retry attempts for password verification
- Admin-exclusive permission: Modify user roles (normal ↔ admin)

### 2. Book Management (Admin Only)
- Add new books with 13-digit ISBN uniqueness validation
- Delete books (with check for borrowed status to prevent invalid deletion)
- Update book information (title/author/publish date)
- Multi-dimensional book search (by ISBN/title/author keywords)
- View all books sorted by ISBN (via BST inorder traversal)

### 3. Borrow & Return Functionality
- Borrow limit: 5 books max for normal users (unlimited for admins)
- Automatic queueing when book stock is 0 (FIFO mechanism)
- Auto-process queue: Next user in queue gets the book after return
- Real-time stock and book status (Available/Unavailable) update

### 4. Data Structures
- **Binary Search Tree (BST)**: Store books for O(logn) efficient ISBN-based search/sort
- **Queue**: Manage borrowing queue with FIFO principle for fair resource allocation

## Running the System

### Prerequisites
- Python 3.7+ (no external dependencies required)

### Execution Steps
1. Navigate to the project directory:
   ```bash
   cd library_management_system
   ```

2. Run the main program:
   ```bash
   python main.py
   ```

3. Follow the on-screen menu prompts to interact with the system

## Test Scenarios

### Basic Test Flow
1. **Admin Login**  
   - Username: `admin`  
   - Password: `admin123`

2. **Add a Test Book**  
   Fill in the following information when prompted:
   - ISBN: 9787115588888
   - Title: Python Programming
   - Author: Ethan
   - Publish Date: 2024-01-01
   - Stock: 2

3. **Register a Normal User**  
   - Username: `user1`  
   - Password: `123456`  
   - Role: `normal` (default)

4. **User Operations**
   - Log in with `user1` credentials
   - Borrow book (ISBN: 9787115588888) → Stock reduces to 1
   - Use another user (`user2`) to borrow the same book → Stock reduces to 0, auto-queue
   - `user1` returns the book → Stock restores to 1, `user2` auto-borrows the book

## Technical Highlights
- **Full OOP Implementation**: Encapsulation, inheritance, polymorphism, abstract base classes (ABC)
- **Efficient Data Handling**: BST for sorted book storage, Queue for borrowing management
- **Robust Validation**: ISBN format check, stock boundary checks, permission verification
- **Layered Architecture**: Clear separation of Model (data) → Service (logic) → UI (interaction)

## Important Notes
- ISBN must be a valid 13-digit numeric string
- Normal users cannot borrow more than 5 books at once
- Books with outstanding borrows cannot be deleted
- Login will be temporarily locked after 3 consecutive failed attempts
- All queue operations follow FIFO (First-In-First-Out) principle

---

## License
This project is for educational purposes only. Feel free to modify and extend for learning use.