# Hash Table Implementation
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [None] * self.size

    def _hash(self, key):
        if isinstance(key, str):
            key_int = sum(ord(c) for c in key)
        else:
            key_int = int(key)
        return key_int % self.size

    def insert(self, key, value):
        index = self._hash(key)
        if self.table[index] is None:
            self.table[index] = Node(key, value)
        else:
            current = self.table[index]
            while current.next:
                if current.key == key:
                    current.value = value
                    return
                current = current.next
            if current.key == key:
                current.value = value
            else:
                current.next = Node(key, value)

    def search(self, key):
        index = self._hash(key)
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def delete(self, key):
        index = self._hash(key)
        current = self.table[index]
        prev = None
        while current:
            if current.key == key:
                if prev is None:
                    self.table[index] = current.next
                else:
                    prev.next = current.next
                return True
            prev = current
            current = current.next
        return False

# Dijkstra's Algorithm Implementation
def dijkstra(graph, start):
    V = len(graph)
    INF = float('inf')
    dist = [INF] * V
    dist[start] = 0
    visited = [False] * V

    for _ in range(V):
        min_dist = INF
        u = -1
        for i in range(V):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i
        if u == -1:
            break
        visited[u] = True
        for v in range(V):
            if not visited[v] and graph[u][v] != 0 and dist[u] + graph[u][v] < dist[v]:
                dist[v] = dist[u] + graph[u][v]
    return dist

# Test Example
if __name__ == "__main__":
    # Test Hash Table
    ht = HashTable()
    ht.insert("9780134685991", "Introduction to Algorithms")
    ht.insert("9781449355739", "Python Programming")
    print("Search 9780134685991:", ht.search("9780134685991"))

    # Test Dijkstra
    library_graph = [
        [0, 5, 10],
        [5, 0, 2],
        [10, 2, 0]
    ]
    print("Shortest distance from A:", dijkstra(library_graph, 0))
