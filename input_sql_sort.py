from collections import defaultdict, deque
import re

def parse_sql_file(sql_file_path):
    """
    Parses an SQL file to extract CREATE TABLE statements and their dependencies.
    Returns a dictionary mapping table names to their dependencies.
    """
    with open(sql_file_path, 'r') as file:
        sql_content = file.read()
    
    # Extract CREATE TABLE statements
    create_statements = re.findall(r'CREATE TABLE\s+(\w+)\s+\((.*?)\);', sql_content, re.S)
    
    dependencies = defaultdict(list)
    for table, body in create_statements:
        # Find all foreign key references
        foreign_keys = re.findall(r'FOREIGN KEY.*?REFERENCES\s+(\w+)', body, re.S)
        dependencies[table].extend(foreign_keys)
    
    return dependencies, dict(create_statements)

def topological_sort(dependencies):
    """
    Perform a topological sort on the tables based on their dependencies.
    """
    # Calculate in-degrees
    in_degree = {table: 0 for table in dependencies}
    for table, deps in dependencies.items():
        for dep in deps:
            in_degree[dep] += 1
    
    # Use a queue to perform Kahn's Algorithm
    queue = deque([table for table, deg in in_degree.items() if deg == 0])
    sorted_tables = []
    
    while queue:
        current = queue.popleft()
        sorted_tables.append(current)
        
        for neighbor in dependencies[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check for cycles
    if len(sorted_tables) != len(in_degree):
        raise ValueError("Cycle detected in table dependencies!")
    
    return sorted_tables

def generate_sorted_sql(sorted_tables, create_statements):
    """
    Generates the sorted SQL CREATE TABLE statements.
    """
    return "\n\n".join(f"CREATE TABLE {table} ({create_statements[table]});" for table in sorted_tables)

# Main function
def main(sql_file_path, output_file_path):
    dependencies, create_statements = parse_sql_file(sql_file_path)
    sorted_tables = topological_sort(dependencies)
    sorted_sql = generate_sorted_sql(sorted_tables, create_statements)
    
    with open(output_file_path, 'w') as output_file:
        output_file.write(sorted_sql)
    print(f"Sorted SQL written to {output_file_path}")

# Example usage
if __name__ == "__main__":
    main('tables.sql', 'sorted_tables.sql')
