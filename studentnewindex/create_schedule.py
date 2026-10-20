import sqlite3

# Connect to the existing database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Create the 'schedule' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        course_code TEXT NOT NULL,
        course_name TEXT NOT NULL,
        semester TEXT NOT NULL,
        section TEXT,
        time TEXT,
        FOREIGN KEY (student_id) REFERENCES students(student_id)
    );
""")

conn.commit()
conn.close()

print("Schedule table created successfully.")

