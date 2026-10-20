# gpa_calculator.py

GRADE_POINTS = {
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D": 1.0,
    "F": 0.0
}

def calculate_projected_gpa(current_gpa, completed_credits, new_courses):
    """
    new_courses: List of tuples -> (course_title, expected_grade, course_credits)
    Example: [("Network Security", "A", 3), ("Ethics", "B+", 2)]
    """
    total_new_points = 0
    total_new_credits = 0

    for title, grade, credits in new_courses:
        grade_point = GRADE_POINTS.get(grade.upper())
        if grade_point is None:
            raise ValueError(f"Invalid grade: {grade}")
        total_new_points += grade_point * credits
        total_new_credits += credits

    total_points = current_gpa * completed_credits + total_new_points
    total_credits = completed_credits + total_new_credits

    projected_gpa = total_points / total_credits if total_credits > 0 else current_gpa
    return round(projected_gpa, 2)

def calculate_required_grade_to_reach_gpa(current_gpa, completed_credits, upcoming_courses, target_gpa):
    total_new_credits = sum(credits for _, credits in upcoming_courses)
    if total_new_credits == 0:
        raise ValueError("Total new credits cannot be zero.")

    total_credits_after = completed_credits + total_new_credits
    required_total_points = target_gpa * total_credits_after
    current_total_points = current_gpa * completed_credits
    required_new_points = required_total_points - current_total_points

    required_avg = required_new_points / total_new_credits

    if required_avg > 4.0:
        return {
            "status": "unachievable",
            "required_avg": required_avg,
            "message": (
                f"🎯 To reach a GPA of {target_gpa}, you’d need an average of {required_avg:.2f}, "
                "which is not possible since 4.0 is the maximum grade point."
            )
        }
    
    return {
        "status": "achievable",
        "required_avg": round(required_avg, 2),
        "message": (
            f"🎯 To reach a GPA of {target_gpa}, you need to average about {required_avg:.2f} GPA points."
        )
    }
