import sqlite3

# Connect to the database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Fetch all rows from the students table
cursor.execute("SELECT * FROM schedule")
rows = cursor.fetchall()

# Get column names
column_names = [description[0] for description in cursor.description]

# Print using tabulate (you can install it with `pip install tabulate`)
for row in rows:
    print(dict(zip(column_names, row)))

# Close the connection
conn.close()

