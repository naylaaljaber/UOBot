import sqlite3

# Connect to the database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Step 1: Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Step 2: Loop through tables and print their contents
for table_name in tables:
    table = table_name[0]
    print(f"\n--- Contents of table: {table} ---")

    try:
        # Fetch all rows
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()

        # Get column names
        column_names = [description[0] for description in cursor.description]

        # Print each row as a dictionary
        for row in rows:
            print(dict(zip(column_names, row)))

    except Exception as e:
        print(f"Error reading table {table}: {e}")

# Close the connection
conn.close()

