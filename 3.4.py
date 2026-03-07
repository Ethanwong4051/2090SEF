def dijkstra(graph, start):
    """
    Dijkstra's Algorithm: single-source shortest path (adjacency matrix implementation)
    :param graph: Adjacency matrix (2D list), graph[i][j] is the weight from node i to j (0 for self, ∞ for no edge)
    :param start: Starting node index (e.g., 0 for reading area A)
    :return: dist: list, dist[i] is the shortest distance from start to node i
    """
    V = len(graph)  # Number of nodes (library reading areas)
    INF = float('inf')
    dist = [INF] * V  # Initialize distance array: infinity for all nodes
    dist[start] = 0  # Distance from start to self is 0
    visited = [False] * V  # Visited node set: False = unvisited
 
    for _ in range(V):
        # Step 1: Find the unvisited node with the minimum current distance
        min_dist = INF
        u = -1
        for i in range(V):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i
 
        if u == -1:
            break  # No reachable unvisited nodes, exit
        visited[u] = True  # Mark node u as visited
 
        # Step 2: Relaxation operation: update distance to adjacent nodes
        for v in range(V):
            # Update condition: unvisited + has edge + new distance is smaller
            if not visited[v] and graph[u][v] != 0 and dist[u] + graph[u][v] < dist[v]:
                dist[v] = dist[u] + graph[u][v]
    return dist
 
# Example: Library reading area network (adjacency matrix)
# Nodes: 0=A,1=B,2=C; graph[i][j] = time cost (minutes), 0=self, INF=no edge
library_graph = [
    [0, 5, 10],
    [5, 0, 2],
    [10, 2, 0]
]
# Find shortest path from A (0) to all nodes
shortest_dist = dijkstra(library_graph, 0)
print("Shortest time cost from area A to each area:", shortest_dist)  # Output: [0,5,7]
