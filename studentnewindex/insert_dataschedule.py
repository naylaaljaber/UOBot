import sqlite3

# Schedule data to insert
schedule_entries = [
    ("202400123", "ENGL 155", "Language Development II", "Year 1 - semester 2", "Section 1", "12:00 - 12:50")
]

# Insert into DB
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.executemany("""
    INSERT INTO schedule (student_id, course_code, course_name, semester, section, time)
    VALUES (?, ?, ?, ?, ?, ?)
""", schedule_entries)

conn.commit()
conn.close()

print("Schedule entries inserted successfully.")

