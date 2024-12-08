# **SQL Dependency Resolver and Cycle Detection**

This repository provides tools for managing SQL table creation order by resolving foreign key dependencies and detecting cyclic relationships. It ensures a correct execution order for `CREATE TABLE` statements and supports multiple input formats like raw SQL or JSON.

---

## **Features**

- **Dependency-Based Sorting**: Automatically sorts `CREATE TABLE` statements to respect foreign key constraints.
- **Cycle Detection**: Identifies and reports cyclic dependencies between tables.
- **Multiple Input Formats**:
  - **Raw SQL**: Parse and sort unsorted SQL `CREATE TABLE` statements.
  - **JSON**: Define tables and relationships in a structured JSON format.
- **Topological Sorting**: Implements efficient graph-based algorithms (e.g., Kahn’s Algorithm) for sorting.

---

## **Quick Start**

1. **Prepare Input**:

   - Provide an unsorted SQL file or a structured JSON file describing tables and dependencies.

2. **Run the Script**:

   ```bash
   python sql_sorter.py --input input_file.sql --output sorted_file.sql
   ```

3. **Output**:

   - A dependency-resolved SQL file ready for execution.

4. **Cycle Detection**:
   - The script automatically detects and reports any cyclic dependencies.
