import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT UNIQUE,
    name TEXT,
    major TEXT,
    gpa REAL,
    total_credits_completed INTEGER,
    current_semester TEXT,
    password_hash TEXT
)
''')

cursor.execute('''
CREATE TABLE courses_completed (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT,
    course_code TEXT,
    course_title TEXT,
    grade TEXT,
    credits INTEGER,
    semester TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
)
''')

conn.commit()
conn.close()

