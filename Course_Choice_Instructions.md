 # Course Choice Instructions

 This document outlines the steps and data structures required to:
 1. Extract course information from PDFs or Markdown files.
 2. Aggregate course data into a CSV for easy machine processing.
 3. Define student preferences in a JSON file.
 4. Define certificate rules in a JSON file.
 5. Implement optimization algorithms to assist in course selection.

 ## 1. Extracting Course Information

 - Navigate to the `Courses/` folder.
 - For each semester subfolder (e.g., `fall2025/`, `summer2025/`, `winter2026/`):
   - Check for existing Markdown files for that semester.
   - If Markdown files do not exist or are empty, run the PDF-to-Markdown conversion script, e.g.:
     ```bash
     python pdf_to_md/converter.py Courses/fall2025/fall2025_all.pdf
     ```
   - Collect all resulting `.md` files for that semester.
 - Parse each Markdown file to extract:
   - Course code and title
   - Block/category (e.g., Mandatory, Optional)
   - Days offered (e.g., Monday, Tuesday)
   - Semester offered (e.g., Fall 2025)
   - Additional metadata as needed
 - Aggregate all extracted data into a single CSV file (`courses.csv`) with columns:
   `course_code,course_title,block,day_offered,semester,additional_info`
 - Additionally, generate a JSON file per semester (e.g., `fall2025_courses.json`) containing an array of course objects following the `template.json` schema.

 ## Course JSON Template (`template.json`)

 Create a `template.json` file describing the structure of a course object:

 ```json
 {
   "course_code": "",
   "course_title": "",
   "block": "",
   "semester": "",
   "days_offered": [],
   "sessions": [],
   "credits": null,
   "prerequisites": [],
   "description": "",
   "location": "",
   "instructor": "",
   "additional_info": ""
 }
 ```

 The fields represent:
 - `course_code`: Course code (e.g., "CS101").
 - `course_title`: Course title.
 - `block`: Category/block (e.g., "Mandatory", "Optional").
 - `semester`: Session when this course is offered (e.g., "Fall2025").
 - `days_offered`: List of weekdays the course meets.
 - `sessions`: List of semesters when the course is available.
 - `credits`: Number of credits.
 - `prerequisites`: List of prerequisite course codes.
 - `description`: Course description text.
 - `location`: Classroom or mode of delivery.
 - `instructor`: Instructor name.
 - `additional_info`: Any other relevant information.

 ## 2. Student Preferences (`student.json`)

 Create a `student.json` file to capture individual student data:
 ```json
 {
   "student_name": "Jane Doe",
   "courses_taken": ["CS101", "MATH200"],
   "preferred_days": ["Monday", "Wednesday", "Friday"]
 }
 ```

 - `student_name`: Full name of the student.
 - `courses_taken`: List of course codes already completed.
 - `preferred_days`: List of days the student prefers to take courses.

 ## 3. Certificate Rules (`certificate_rules.json`)

 Define program requirements in `certificate_rules.json`:
 ```json
 {
   "rules": [
     {
       "type": "mandatory",
       "block": "Fundamentals",
       "required": 5
     },
     {
       "type": "elective",
       "block": "Advanced Topics",
       "choose": 2,
       "from": ["CS300", "CS310", "CS320"]
     }
   ]
 }
 ```

 - **Mandatory**: Must take a fixed number of courses from a specific block.
 - **Elective**: Choose a subset of courses from a block.

 ## 4. Optimization Algorithm

 Using `courses.csv`, `student.json`, and `certificate_rules.json`:
 1. Filter out courses already taken.
 2. Prioritize mandatory courses not yet completed.
 3. Apply availability and preferences:
    - Courses offered in limited sessions get higher priority.
    - Match with `preferred_days`.
 4. Solve as a constrained optimization problem to:
    - Satisfy certificate rules.
    - Maximize alignment with preferences and availability.

 ## 5. Next Steps

 - Implement scripts to automate:
   - Markdown conversion
   - CSV aggregation
   - JSON parsing
   - Optimization (e.g., via integer linear programming)