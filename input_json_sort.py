import json
from collections import defaultdict, deque

def parse_json(json_file_path):
    """
    Parse the JSON file containing table definitions.
    Returns a dictionary mapping table names to their dependencies and table definitions.
    """
    with open(json_file_path, 'r') as file:
        table_definitions = json.load(file)

    dependencies = defaultdict(list)
    table_data = {}
    
    for table in table_definitions:
        table_name = table['table_name']
        table_data[table_name] = table
        
        # Collect dependencies from foreign keys
        for foreign_key in table.get('foreign_keys', []):
            dependencies[table_name].append(foreign_key['reference'])
    
    return dependencies, table_data

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

def generate_sorted_sql(sorted_tables, table_data):
    """
    Generate sorted SQL `CREATE TABLE` statements.
    """
    sql_statements = []
    
    for table_name in sorted_tables:
        table = table_data[table_name]
        
        columns = ',\n    '.join(table['columns'])
        primary_keys = ', '.join(table.get('primary_keys', []))
        primary_key_clause = f",\n    PRIMARY KEY ({primary_keys})" if primary_keys else ""
        
        foreign_keys = [
            f"FOREIGN KEY ({fk['column']}) REFERENCES {fk['reference']}({fk['reference_column']})"
            for fk in table.get('foreign_keys', [])
        ]
        foreign_key_clause = f",\n    " + ',\n    '.join(foreign_keys) if foreign_keys else ""
        
        create_statement = f"CREATE TABLE {table_name} (\n    {columns}{primary_key_clause}{foreign_key_clause}\n);"
        sql_statements.append(create_statement)
    
    return "\n\n".join(sql_statements)

def main(json_file_path, output_file_path):
    dependencies, table_data = parse_json(json_file_path)
    sorted_tables = topological_sort(dependencies)
    sorted_sql = generate_sorted_sql(sorted_tables, table_data)
    
    with open(output_file_path, 'w') as output_file:
        output_file.write(sorted_sql)
    print(f"Sorted SQL written to {output_file_path}")

# Example usage
if __name__ == "__main__":
    main('tables.json', 'sorted_tables.sql')
