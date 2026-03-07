# Study Report

**Course:** COMP2090SEF Data Structures, Algorithms and Problem Solving

**Topic:** Hash Table (Data Structure) & Dijkstra’s Algorithm (Algorithm)

**Submission Date:** 2026/3/6

## 1. Introduction
This report focuses on self-studying Hash Table (a new data structure) and Dijkstra’s Algorithm (a new algorithm) that are not covered in the course curriculum. The hash table is selected for its high-efficiency key-value search and storage characteristics, which can be applied to optimize the book information query in the library management system (reducing query time from O(n) to nearly O(1)). Dijkstra’s Algorithm is a classic shortest path algorithm, which is introduced for its wide application in graph-based resource scheduling and can be extended to the library’s book borrowing path planning and resource allocation optimization. Both the data structure and the algorithm are implemented in Python, combined with practical application scenarios of the library management system for verification and analysis.

## 2. New Data Structure: Hash Table
### 2.1 Abstract Data Type (ADT) Definition
The hash table is a non-linear data structure that maps keys to values through a hash function, realizing direct access to data. Its core ADT includes the following basic operations:
- **hash(key):** Converts the input key into a non-negative integer index.
- **insert(key, value):** Inserts the key-value pair into the hash table.
- **search(key):** Queries the corresponding value.
- **delete(key):** Deletes the key-value pair.
- **is_empty():** Checks whether the hash table is empty.

### 2.2 Core Implementation: Hash Function & Conflict Resolution
- **Hash Function:** Uses modulo operation. String keys are converted to integers by summing ASCII values.
- **Conflict Resolution:** Uses separate chaining with linked lists.

### 2.3 Application Scenario in Library Management System
- Uses ISBN as key and book info as value.
- Achieves O(1) average query time.
- Can extend to user information management.

### 2.4 Python Code Implementation (Core Snippets)
```python
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
```
## 3. New Algorithm: Dijkstra’s Algorithm
### 3.1 Core Concept & Application Scenario
Dijkstra’s Algorithm finds the shortest path from a starting node to all other nodes in a weighted graph with non-negative edges.

Applications in library system include:

Modeling reading areas as nodes.

Finding minimum-cost borrowing paths.

Optimizing book allocation scheduling.

### 3.2 Time Complexity Analysis
Basic Implementation: O(V²) using adjacency matrix.

Optimized Implementation: O((V+E)logV) using min-heap.

Space Complexity: O(V).

### 3.3 Execution Steps Example
Initialize distances.

Select minimum-distance unvisited node.

Relax edges.

Repeat until all nodes visited.

Output shortest paths.

### 3.4 Python Implementation (O(V²))
```python
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
Example graph:

python
library_graph = [
    [0, 5, 10],
    [5, 0, 2],
    [10, 2, 0]
]
```
## 4. Integration with Library Management System
Hash Table replaces BST for book storage.

Dijkstra’s Algorithm added for path planning.

Encapsulated into system modules for reuse.

## 5. References
Maurer, Lewis. Hash table methods. ACM Computing Surveys, 1975.

Larson. Dynamic hash tables. CACM, 1988.

Fan & Shi. Improvement of Dijkstra's algorithm, 2010.

Wang. Improved Dijkstra's shortest path algorithm, 2012.