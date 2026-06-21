import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def get_student_transcript(student_id: str) -> dict:
    """
    Fetches the academic transcript for a given student ID.
    Returns their major and a list of courses they have completed.
    """
    students_file = os.path.join(DATA_DIR, 'students.json')
    try:
        with open(students_file, 'r') as f:
            students = json.load(f)
    except FileNotFoundError:
        return {"error": "Student database not found."}
        
    for student in students:
        if student['student_id'] == student_id:
            return {
                "student_name": student["student_name"],
                "major": student["major"],
                "courses_completed": student["courses_completed"]
            }
            
    return {"error": f"Student ID {student_id} not found."}

def get_course_info(course_id: str) -> dict:
    """
    Fetches information about a specific course, including its name, 
    credits, semesters offered, and prerequisites.
    """
    courses_file = os.path.join(DATA_DIR, 'courses.json')
    try:
        with open(courses_file, 'r') as f:
            courses = json.load(f)
    except FileNotFoundError:
        return {"error": "Course database not found."}
        
    for course in courses:
        if course['course_id'] == course_id:
            return course
            
    return {"error": f"Course ID {course_id} not found."}
    
def get_all_courses() -> list:
    """
    Returns a list of all available course IDs and their names.
    """
    courses_file = os.path.join(DATA_DIR, 'courses.json')
    try:
        with open(courses_file, 'r') as f:
            courses = json.load(f)
    except FileNotFoundError:
        return []
        
    return [{"course_id": c["course_id"], "course_name": c["course_name"]} for c in courses]

def get_degree_requirements(major: str) -> dict:
    """
    Fetches the degree requirements for a specific major.
    Returns the core required courses, the number of electives needed, 
    and the pool of allowed electives.
    """
    curriculum_file = os.path.join(DATA_DIR, 'curriculum.json')
    try:
        with open(curriculum_file, 'r') as f:
            curriculums = json.load(f)
    except FileNotFoundError:
        return {"error": "Curriculum database not found."}
        
    if major in curriculums:
        return curriculums[major]
    else:
        return {"error": f"Major '{major}' not found in curriculum database."}
