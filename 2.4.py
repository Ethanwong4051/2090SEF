class Node:
 # Node class for chaining: store key, value and next node pointer
 Def_init_(self, key, value):
 self.key = key
 self.value = value
 self.next = None
class HashTable:
 Def_init_(self, size=100):
self.size = size # Hash table size, default 100 (suitable for library book scale)
self.table = [None] * self.size # Initialize hash table with empty linked list heads
def _hash(self, key):
        # Private hash function: convert key to index
        if isinstance(key, str):
            # Convert string key (ISBN) to integer: sum ASCII values of each character
            key_int = sum(ord(c) for c in key)
        else:
            key_int = int(key)
        return key_int % self.size  # Modulo operation to get index
 
    def insert(self, key, value):
        # Insert key-value pair: resolve conflict by chaining
        index = self._hash(key)
        if self.table[index] is None:
            self.table[index] = Node(key, value)  # No conflict: directly create node
        else:
            # Conflict: traverse to the end of the linked list and add new node
            current = self.table[index]
            while current.next:
                if current.key == key:
                    current.value = value  # Overwrite if key exists (update book info)
                    return
                current = current.next
            if current.key == key:
                current.value = value
            else:
                current.next = Node(key, value)
 
    def search(self, key):
        # Query value by key: core function for library book search
        index = self._hash(key)
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value  # Return book info if key matches
            current = current.next
        return None  # Return None if book does not exist
 
    def delete(self, key):
        # Delete key-value pair: remove book info from the system
        index = self._hash(key)
        current = self.table[index]
        prev = None
        while current:
            if current.key == key:
                if prev is None:
                    self.table[index] = current.next  # Delete head node
                else:
                    prev.next = current.next  # Delete middle/tail node
                return True
            prev = current
            current = current.next
        return False  # Return False if key does not exist
