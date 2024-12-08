def detect_cycle(graph):
    """
    Detect cycles in a directed graph using DFS.
    
    Parameters:
    - graph (dict): A dictionary where keys are nodes and values are lists of adjacent nodes.
    
    Returns:
    - bool: True if a cycle is detected, False otherwise.
    """
    visited = set()
    recursion_stack = set()

    def dfs(node):
        if node in recursion_stack:  # Cycle detected
            return True
        if node in visited:  # Already visited, no cycle from this node
            return False

        # Mark the current node as visited and add to recursion stack
        visited.add(node)
        recursion_stack.add(node)

        # Visit all neighbors
        for neighbor in graph.get(node, []):
            if dfs(neighbor):  # If a cycle is found in any neighbor, propagate it
                return True

        # Remove the node from the recursion stack
        recursion_stack.remove(node)
        return False

    # Check each node in the graph
    for node in graph:
        if dfs(node):
            return True  # Cycle detected

    return False  # No cycle detected
