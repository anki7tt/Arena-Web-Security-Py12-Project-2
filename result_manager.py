import csv
import os
from typing import List, Optional, Tuple, Dict
from student import Student


class ResultManager:
    def __init__(self, csv_filepath: str = "students_data.csv"):
        self.students: Dict[str, Student] = {}
        self.csv_filepath = csv_filepath

    def add_student(self, student: Student) -> Tuple[bool, str]:
        if not isinstance(student, Student):
            return False, "Invalid object: Must be an instance of Student."

        cleaned_id = student.student_id.strip()
        if not cleaned_id:
            return False, "Student ID cannot be empty."

        if not student.name.strip():
            return False, "Student name cannot be empty."

        for existing_id in self.students.keys():
            if existing_id.lower() == cleaned_id.lower():
                return False, f"Student with ID '{cleaned_id}' already exists."

        self.students[cleaned_id] = student
        return True, f"Student '{student.name}' (ID: {cleaned_id}) added successfully."

    def search_student(self, student_id: str) -> Optional[Student]:
        query = str(student_id).strip().lower()
        for s_id, student in self.students.items():
            if s_id.lower() == query:
                return student
        return None

    def get_all_students(self) -> List[Student]:
        return list(self.students.values())

    def get_total_count(self) -> int:
        return len(self.students)

    def get_highest_scorer(self) -> Optional[Student]:
        if not self.students:
            return None
        return max(self.students.values(), key=lambda s: s.calculate_total())

    def get_lowest_scorer(self) -> Optional[Student]:
        if not self.students:
            return None
        return min(self.students.values(), key=lambda s: s.calculate_total())

    def generate_class_summary(self) -> Optional[Dict]:
        if not self.students:
            return None

        students_list = list(self.students.values())
        total_students = len(students_list)

        passed_students = [s for s in students_list if s.get_status() == "Pass"]
        failed_students = [s for s in students_list if s.get_status() == "Fail"]

        total_marks_list = [s.calculate_total() for s in students_list]
        avg_percentages = [s.calculate_percentage() for s in students_list]

        class_avg_total = round(sum(total_marks_list) / total_students, 2)
        class_avg_percentage = round(sum(avg_percentages) / total_students, 2)

        pass_count = len(passed_students)
        fail_count = len(failed_students)
        pass_rate = round((pass_count / total_students) * 100.0, 2)
        fail_rate = round((fail_count / total_students) * 100.0, 2)

        grades = ["A+", "A", "B", "C", "D", "E", "F"]
        grade_distribution = {g: 0 for g in grades}
        for s in students_list:
            g = s.calculate_grade()
            if g in grade_distribution:
                grade_distribution[g] += 1
            else:
                grade_distribution[g] = 1

        subject_stats = {}
        for subj in Student.DEFAULT_SUBJECTS:
            subj_marks = [s.marks.get(subj, 0.0) for s in students_list if subj in s.marks]
            if subj_marks:
                subject_stats[subj] = {
                    "average": round(sum(subj_marks) / len(subj_marks), 2),
                    "highest": round(max(subj_marks), 2),
                    "lowest": round(min(subj_marks), 2),
                }

        highest_student = self.get_highest_scorer()
        lowest_student = self.get_lowest_scorer()

        return {
            "total_students": total_students,
            "passed_count": pass_count,
            "failed_count": fail_count,
            "pass_rate": pass_rate,
            "fail_rate": fail_rate,
            "class_avg_total": class_avg_total,
            "class_avg_percentage": class_avg_percentage,
            "highest_student": highest_student,
            "lowest_student": lowest_student,
            "grade_distribution": grade_distribution,
            "subject_stats": subject_stats
        }

    def save_to_csv(self, filepath: Optional[str] = None) -> Tuple[bool, str]:
        target_path = filepath or self.csv_filepath

        if not self.students:
            return False, "No student data to save. The list is empty."

        fieldnames = [
            "Student ID", "Name",
            "Math", "Science", "English", "History", "Computer",
            "Total Marks", "Average Marks", "Percentage", "Grade", "Status"
        ]

        try:
            with open(target_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

                for student in self.students.values():
                    row = {
                        "Student ID": student.student_id,
                        "Name": student.name,
                        "Math": student.marks.get("Math", 0.0),
                        "Science": student.marks.get("Science", 0.0),
                        "English": student.marks.get("English", 0.0),
                        "History": student.marks.get("History", 0.0),
                        "Computer": student.marks.get("Computer", 0.0),
                        "Total Marks": student.calculate_total(),
                        "Average Marks": student.calculate_average(),
                        "Percentage": student.calculate_percentage(),
                        "Grade": student.calculate_grade(),
                        "Status": student.get_status()
                    }
                    writer.writerow(row)

            return True, f"Successfully saved {len(self.students)} records to '{target_path}'."
        except Exception as e:
            return False, f"Failed to save CSV file: {str(e)}"

    def load_from_csv(self, filepath: Optional[str] = None) -> Tuple[bool, str]:
        target_path = filepath or self.csv_filepath

        if not os.path.exists(target_path):
            return False, f"File '{target_path}' does not exist."

        loaded_count = 0
        skipped_count = 0

        try:
            with open(target_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                if not reader.fieldnames:
                    return False, f"CSV file '{target_path}' is empty."

                required = {"Student ID", "Name"}
                if not required.issubset(set(reader.fieldnames)):
                    return False, f"CSV is missing required headers: {required - set(reader.fieldnames)}"

                for row in reader:
                    s_id = row.get("Student ID", "").strip()
                    s_name = row.get("Name", "").strip()

                    if not s_id or not s_name:
                        skipped_count += 1
                        continue

                    marks = {}
                    for subj in Student.DEFAULT_SUBJECTS:
                        raw_val = row.get(subj, "0").strip()
                        try:
                            val = float(raw_val)
                            marks[subj] = max(0.0, min(100.0, val))
                        except ValueError:
                            marks[subj] = 0.0

                    student = Student(student_id=s_id, name=s_name, marks=marks)
                    self.students[s_id] = student
                    loaded_count += 1

            status_msg = f"Loaded {loaded_count} student(s) from '{target_path}'."
            if skipped_count > 0:
                status_msg += f" ({skipped_count} invalid rows skipped)."
            return True, status_msg

        except Exception as e:
            return False, f"Error reading CSV file: {str(e)}"
