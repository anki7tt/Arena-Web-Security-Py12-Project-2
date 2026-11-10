# 🎓 Coaching Center Student Result Management System

A robust, terminal-based, Object-Oriented Python application designed for coaching centers and educational institutions to manage student marks, calculate grades, evaluate pass/fail standing, track top/lowest performers, generate comprehensive batch analytics, and persist records in CSV format.

---

## 📋 Table of Contents
1. [Overview & Project Scenario](#overview--project-scenario)
2. [Key Features](#key-features)
3. [System Architecture & OOP Design](#system-architecture--oop-design)
4. [Grading & Pass/Fail Rules](#grading--passfail-rules)
5. [Project Structure](#project-structure)
6. [Prerequisites & Installation](#prerequisites--installation)
7. [How to Run](#how-to-run)
8. [Automated Testing](#automated-testing)

---

## 📖 Overview & Project Scenario
Coaching centers need to track the academic performance of students enrolled in various subjects. Calculating results manually is prone to human error, time-consuming, and difficult to audit.

This system provides:
- Automated calculation of **Total Marks**, **Average Marks**, **Percentages**, and **Grades**.
- Intelligent **Pass/Fail conditional logic** based on subject-level and overall benchmarks.
- Instant search and retrieval of individual student report cards.
- Identification of **Highest-Scoring** and **Lowest-Scoring** students.
- Whole-class statistical summaries including pass rates, grade distributions, and subject averages.
- Persistent file storage using **CSV** so that student records are retained across program sessions.

---

## ✨ Key Features
- **Object-Oriented Programming (OOP):** Modular architecture cleanly divided between data modeling (`Student`) and data orchestration (`ResultManager`).
- **5 Core Subjects Tracked:** Mathematics, Science, English, History, and Computer.
- **Detailed Report Card View:** Individual performance cards showing marks, percentage, grade, and passing status per subject.
- **Batch Performance Analytics:** Class average, pass/fail percentages, grade frequency chart, and subject-wise high/low/average breakdown.
- **Persistent CSV Storage (Bonus Challenge):** Auto-load existing records on startup and manual Save/Load capabilities.
- **Robust Error Handling:** Zero crashes on non-numeric inputs, negative marks, duplicate IDs, empty values, or missing files.
- **Zero External Dependencies:** Built entirely with Python's built-in standard library (`csv`, `os`, `sys`, `unittest`).

---

## 🏗️ System Architecture & OOP Design

### 1. `Student` Class (`student.py`)
Encapsulates an individual student's identity, enrolled marks, and calculation logic.

- **Attributes:**
  - `student_id` *(str)*: Unique alphanumeric identifier (e.g., `S101`).
  - `name` *(str)*: Student's full name.
  - `marks` *(dict)*: Dictionary mapping subject name to numeric score (`0.0` - `100.0`).

- **Methods:**
  - `set_mark(subject, mark)`: Validates and assigns mark with range verification (`0 <= mark <= 100`).
  - `calculate_total()`: Returns sum of all 5 subject marks (maximum 500).
  - `calculate_average()`: Returns mean score across all subjects.
  - `calculate_percentage()`: Returns percentage relative to maximum marks.
  - `calculate_grade()`: Returns letter grade (`A+`, `A`, `B`, `C`, `D`, `E`, `F`).
  - `get_failed_subjects()`: Returns list of subjects where mark is strictly `< 40.0`.
  - `get_status()`: Evaluates whether student passes or fails.
  - `to_dict()`: Serializes student profile to a dictionary for reporting and CSV output.

### 2. `ResultManager` Class (`result_manager.py`)
Responsible for managing the collection of students, querying data, calculating aggregate statistics, and handling CSV persistence.

- **Attributes:**
  - `students` *(dict)*: Key-value map of `{student_id: Student_Object}` for $O(1)$ search and instant uniqueness validation.
  - `csv_filepath` *(str)*: Target path for persistent database storage.

- **Methods:**
  - `add_student(student)`: Enforces unique student ID and non-empty inputs.
  - `search_student(student_id)`: Case-insensitive search by student ID.
  - `get_highest_scorer()`: Finds student(s) with the highest total score.
  - `get_lowest_scorer()`: Finds student(s) with the lowest total score.
  - `generate_class_summary()`: Computes total students, pass/fail counts, class average, grade distribution, and per-subject statistics.
  - `get_all_students()`: Returns list of all enrolled students.
  - `save_to_csv(filepath)`: Saves records to CSV file using standard `csv.DictWriter`.
  - `load_from_csv(filepath)`: Safely parses CSV records into `Student` objects.

---

## 📊 Grading & Pass/Fail Rules

### Grading Scale:
| Percentage Range | Grade | Performance Level |
| :---: | :---: | :---: |
| **90.0% – 100.0%** | **A+** | Outstanding |
| **80.0% – 89.9%**  | **A**  | Excellent |
| **70.0% – 79.9%**  | **B**  | Very Good |
| **60.0% – 69.9%**  | **C**  | Good |
| **50.0% – 59.9%**  | **D**  | Satisfactory |
| **40.0% – 49.9%**  | **E**  | Pass |
| **Below 40.0%**    | **F**  | Fail |

### Pass / Fail Criteria:
A student is awarded **"Pass"** status if and only if:
1. **Subject-wise passing threshold:** The student scores **at least 40 marks** in *each* of the 5 subjects.
2. **Overall percentage threshold:** The student obtains an aggregate percentage of **at least 40%**.

> *Note:* If a student fails in even one subject (e.g., scores 32 in Math while scoring 90+ in others), their status is marked as **Fail** and their grade is assigned as **F**.

---

## 📁 Project Structure

```text
aws-py12/
│
└── Project 2/                          # Dedicated project folder for submission
    ├── main.py                         # Menu-driven CLI interface
    ├── project_2.py                    # Standalone executable version
    ├── student.py                      # Student class definition
    ├── result_manager.py               # ResultManager class definition
    ├── test_system.py                  # Automated unit and integration test suite
    ├── students_data.csv               # Persistent CSV student database
    └── README.md                       # Complete documentation & viva guide
```

---

## 💻 Prerequisites & Installation

### Prerequisites:
- Python 3.8 or higher installed on your computer.
- No external packages required (no `pip install` needed).

### Verification:
Open your terminal (PowerShell, Command Prompt, or Bash) and check your Python version:
```bash
python --version
```

---

## 🚀 How to Run

### Run from the Project 2 folder:
```bash
cd "Project 2"
python main.py
```
*(or run `python project_2.py`)*

### Interactive Menu Navigation:
```text
========================================================================
      COACHING CENTER - STUDENT RESULT MANAGEMENT SYSTEM        
========================================================================
 [1] Add New Student
 [2] View All Students
 [3] Search Student by ID
 [4] Display Highest & Lowest Scoring Students
 [5] Generate Class Performance Summary
 [6] Save Student Records to CSV (Bonus)
 [7] Load Student Records from CSV (Bonus)
 [8] Exit Application
========================================================================
 Select an option (1-8):
```

---

## 🧪 Automated Testing

The project includes an automated test suite verifying calculations, grade boundaries, edge cases, duplicate rejection, and CSV persistence.

Run the test suite with:
```bash
python "Project 2/test_system.py"
# or when inside the Project 2 folder:
python test_system.py
```

**Expected output:**
```text
Ran 9 tests in 0.014s

OK
```


