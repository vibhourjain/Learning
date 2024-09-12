from flask import Flask, jsonify, request
import json
from datetime import datetime
import os

app = Flask(__name__)

# Define the path to your JSON file
json_file_path = r'C:\Users\vibho\OneDrive\Desktop\VIBHOURJAIN\Vibhour\Learning\RestAPI\students.json'

# Load students data from the JSON file
try:
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            students = json.load(f)  # Ensure 'students' is defined here
        print(f"Loaded students data: {students}")
    else:
        students = []  # Initialize as an empty list if the file doesn't exist
        print(f"File not found: {json_file_path}")
except Exception as e:
    students = []  # Initialize as an empty list in case of any error
    print(f"Error loading file: {e}")

# Function to filter students born between specific dates
def filter_students_by_dob(students, start_date, end_date):
    filtered_students = [
        student for student in students
        if start_date <= datetime.strptime(student["dob"], "%Y-%m-%d") <= end_date
    ]
    return filtered_students

# Function to filter students born in a specific year
def filter_students_by_year(students, year):
    filtered_students = [
        student for student in students
        if datetime.strptime(student["dob"], "%Y-%m-%d").year == year
    ]
    return filtered_students

# Function to get a student by ID
def get_student_by_id(students, student_id):
    for student in students:
        if student["id"] == student_id:
            return student
    return None

# API to get students data
@app.route('/students', methods=['GET'])
def get_students():
    print("Current students data: ", students)
    # Retrieve query parameters
    year = request.args.get('year', type=int)
    student_id = request.args.get('id', type=int)
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    # If student_id is provided, return the specific student's data
    if student_id is not None:
        student = get_student_by_id(students, student_id)
        if student:
            return jsonify(student)
        else:
            return jsonify({"error": "Student not found"}), 404

    # If year is provided, filter students born in that year
    elif year is not None:
        filtered_students = filter_students_by_year(students, year)
        return jsonify(filtered_students)

    # If start_date and end_date are provided, filter students born between those dates
    elif start_date_str and end_date_str:
        try:
            # Convert start_date and end_date to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD"}), 400
        
        # Filter students based on the provided dates
        filtered_students = filter_students_by_dob(students, start_date, end_date)
        return jsonify(filtered_students)

    # If no filter is applied, return all students
    else:
        return jsonify(students)

if __name__ == '__main__':
    app.run(debug=True)
