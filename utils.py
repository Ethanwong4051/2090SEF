def validate_isbn(isbn):
    if not isbn.isdigit():
        return False
    if len(isbn) != 13:
        return False
    return True

def format_isbn(isbn):
    return isbn.replace('-', '').replace(' ', '')

def generate_user_id(counter):
    return f"U{counter:03d}"

def encrypt_password(password):
    import hashlib
    return hashlib.md5(password.encode()).hexdigest()

def load_data():
    pass

def save_data():
    pass