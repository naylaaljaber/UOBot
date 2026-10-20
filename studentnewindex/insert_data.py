import sqlite3

# Connect to the existing database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Student info
student = {
    "student_id": "202100456",
    "name": "Omar Hamad",
    "major": "Networkengineering",
    "gpa": 3.5,
    "total_credits_completed": 53,
    "current_semester": "Year 2 - Semester 1",
    "password_hash": "$2b$12$kN1B31cJw5vsh2zDYtugA.kuoAzmu.tt6EcW2zZ/FN4qR53rfD3z2"
}

# Insert student
cursor.execute("""
    INSERT INTO students (student_id, name, major, gpa, total_credits_completed, current_semester, password_hash)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    student["student_id"],
    student["name"],
    student["major"],
    student["gpa"],
    student["total_credits_completed"],
    student["current_semester"],
    student["password_hash"]
))

# Courses
courses = [
    {"course_code": "ITNE 110", "course_title": "Introduction to Computer and Network Technology", "grade": "A", "credits": 3, "semester": "Year 1 - Semester 1"},
    {"course_code": "ITCS 113", "course_title": "Computer Programming I", "grade": "A", "credits": 3, "semester": "Year 1 - Semester 1"},
    {"course_code": "PHYCS 101", "course_title": "General Physics I", "grade": "B+", "credits": 4, "semester": "Year 1 - Semester 1"},
    {"course_code": "MATHS 101", "course_title": "Calculus I", "grade": "B+", "credits": 3, "semester": "Year 1 - Semester 1"},
    {"course_code": "ENGL 154", "course_title": "Language Development I", "grade": "A", "credits": 3, "semester": "Year 1 - Semester 1"},
    {"course_code": "ITCE 112", "course_title": "Digital Design I", "grade": "B+", "credits": 3, "semester": "Year 1 - Semester 2"},
    {"course_code": "ITCS 114", "course_title": "Computer Programming II", "grade": "A", "credits": 3, "semester": "Year 1 - Semester 2"},
    {"course_code": "PHYCS 102", "course_title": "General Physics II", "grade": "B+", "credits": 4, "semester": "Year 1 - Semester 2"},
    {"course_code": "MATHS 102", "course_title": "Calculus II", "grade": "A", "credits": 3, "semester": "Year 1 - Semester 2"},
    {"course_code": "ENGL 155", "course_title": "Language Development II", "grade": "A", "credits": 3, "semester": "Year 1 - Semester 2"},
    {"course_code": "HRLC 107", "course_title": "Human Rights", "grade": "A", "credits": 2, "semester": "Year 1 - Semester 2"},
    {"course_code": "ITCE 221", "course_title": "Electrical Circuit Analysis", "grade": "B+", "credits": 3, "semester": "Year 2 - Semester 1"},
    {"course_code": "ITNE 231", "course_title": "Computer Networks I", "grade": "A", "credits": 3, "semester": "Year 2 - Semester 1"},
    {"course_code": "ITCS 214", "course_title": "Data Structures", "grade": "A", "credits": 3, "semester": "Year 2 - Semester 1"},
    {"course_code": "MATHS 205", "course_title": "Differential Equations", "grade": "B+", "credits": 3, "semester": "Year 2 - Semester 1"},
    {"course_code": "STAT 273", "course_title": "Probability and Statistics", "grade": "B+", "credits": 3, "semester": "Year 2 - Semester 1"},
    {"course_code": "CHEMY 101", "course_title": "General Chemistry I", "grade": "A", "credits": 4, "semester": "Year 2 - Semester 1"}
]

# Insert courses
for course in courses:
    cursor.execute("""
        INSERT INTO courses_completed (student_id, course_code, course_title, grade, credits, semester)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        student["student_id"],
        course["course_code"],
        course["course_title"],
        course["grade"],
        course["credits"],
        course["semester"]
    ))

# Save and close
conn.commit()
conn.close()

print("Inserted Omar Hamad's data successfully.")

