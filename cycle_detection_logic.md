## **Logic Behind Cycle Detection**

The cycle detection algorithm uses **Depth-First Search (DFS)** to identify cycles in a directed graph. Below is a detailed explanation of the approach:

### **Key Concepts**

1. **Directed Graph**:

   - The graph is represented as an adjacency list, where:
     - Each node points to its adjacent nodes (i.e., nodes it has directed edges toward).
   - Example:
     ```python
     graph = {
         'A': ['B'],
         'B': ['C'],
         'C': ['A']  # Cycle here
     }
     ```

2. **Cycle in a Directed Graph**:

   - A cycle exists if there is a path that starts from a node and eventually leads back to the same node via directed edges.

3. **DFS-Based Detection**:
   - A **back edge** (an edge that points to a previously visited node in the current DFS path) indicates a cycle.

---

### **Algorithm Steps**

1. **Data Structures**:

   - **Visited Set**: Tracks nodes that have been completely processed.
   - **Recursion Stack**: Tracks nodes currently in the DFS call stack to detect back edges.

2. **DFS Traversal**:

   - Start DFS from each unvisited node.
   - For each node:
     - Mark it as visited and add it to the recursion stack.
     - Recursively visit its neighbors.
     - If a neighbor is in the recursion stack, a cycle exists.
     - Once all neighbors are processed, remove the node from the recursion stack.

3. **Cycle Detection**:
   - If any node leads to a back edge (a node already in the recursion stack), the graph contains a cycle.
   - If all nodes are processed without finding a back edge, the graph is acyclic.

---

### **Pseudocode**

```text
function detect_cycle(graph):
    visited = set()           # Set of completely processed nodes
    recursion_stack = set()   # Nodes in the current DFS path

    function dfs(node):
        if node in recursion_stack:  # Back edge detected
            return True
        if node in visited:          # Already processed, no cycle
            return False

        # Mark current node as visited and add to recursion stack
        visited.add(node)
        recursion_stack.add(node)

        # Recursively visit neighbors
        for neighbor in graph[node]:
            if dfs(neighbor):
                return True  # Cycle detected in neighbor

        # Remove node from recursion stack after processing
        recursion_stack.remove(node)
        return False

    # Check all nodes in the graph
    for node in graph.keys():
        if node not in visited:
            if dfs(node):
                return True  # Cycle detected

    return False  # No cycle found
```

---

### **Example**

#### Graph with a Cycle:

```text
Graph:
A -> B -> C -> A

Steps:
1. Start DFS from 'A'.
2. Visit 'B', then 'C', then back to 'A' (already in recursion stack).
3. Cycle detected.
```

#### Graph without a Cycle:

```text
Graph:
A -> B -> C

Steps:
1. Start DFS from 'A'.
2. Visit 'B', then 'C'.
3. No back edges, all nodes processed.
4. No cycle detected.
```

---

### **Complexity Analysis**

- **Time Complexity**: **O(V + E)**
  - \( V \): Number of vertices (nodes).
  - \( E \): Number of edges.
  - Each node and edge is visited at most once during DFS.
- **Space Complexity**: **O(V)**
  - Due to the recursion stack and auxiliary sets.
