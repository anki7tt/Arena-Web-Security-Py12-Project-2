import os
import sys
from student import Student
from result_manager import ResultManager


def print_header(title: str):
    width = 72
    print("\n" + "=" * width)
    print(f" {title.upper()} ".center(width, "="))
    print("=" * width)


def print_divider():
    print("-" * 72)


def get_non_empty_input(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print(" [!] Input cannot be empty. Please try again.")


def get_valid_mark(subject: str) -> float:
    while True:
        raw_val = input(f" -> Enter mark for {subject} (0 - 100): ").strip()
        try:
            val = float(raw_val)
            if 0.0 <= val <= 100.0:
                return round(val, 2)
            else:
                print(f" [!] Mark must be between 0 and 100. You entered: {val}")
        except ValueError:
            print(f" [!] Invalid input '{raw_val}'. Please enter a valid number.")


def display_student_card(student: Student):
    print_divider()
    print(f" Student ID : {student.student_id}")
    print(f" Name       : {student.name}")
    print(" Subject Marks:")
    for subj in Student.DEFAULT_SUBJECTS:
        mark = student.marks.get(subj, 0.0)
        status_tag = "[PASS]" if mark >= student.PASSING_THRESHOLD else "[FAIL]"
        print(f"   - {subj:<15}: {mark:>6.2f} / 100   {status_tag}")
    print_divider()
    print(f" Total Marks: {student.calculate_total():>6.2f} / {len(student.marks)*100:.0f}")
    print(f" Average    : {student.calculate_average():>6.2f}%")
    print(f" Percentage : {student.calculate_percentage():>6.2f}%")
    print(f" Grade      : {student.calculate_grade()}")
    status_str = student.get_status()
    if status_str == "Pass":
        print(f" Status     : \033[92mPASS\033[0m")
    else:
        failed = student.get_failed_subjects()
        failed_info = f" (Failed in: {', '.join(failed)})" if failed else ""
        print(f" Status     : \033[91mFAIL{failed_info}\033[0m")
    print_divider()


def handle_add_student(manager: ResultManager) -> bool:
    print_header("Add New Student")

    while True:
        student_id = get_non_empty_input(" Enter Student ID (e.g. S101): ")
        if manager.search_student(student_id):
            print(f" [!] Error: Student with ID '{student_id}' already exists!")
            retry = input(" Would you like to enter a different ID? (y/n): ").strip().lower()
            if retry != 'y':
                print(" Operation cancelled.")
                return False
        else:
            break

    name = get_non_empty_input(" Enter Student Full Name: ")

    print("\n Enter marks for the 5 subjects:")
    marks = {}
    for subj in Student.DEFAULT_SUBJECTS:
        marks[subj] = get_valid_mark(subj)

    new_student = Student(student_id=student_id, name=name, marks=marks)
    success, msg = manager.add_student(new_student)

    if success:
        print(f"\n [✓] {msg}")
        print("\n Calculated Student Summary:")
        print(f"  • Total Marks : {new_student.calculate_total()}")
        print(f"  • Average     : {new_student.calculate_average()}%")
        print(f"  • Grade       : {new_student.calculate_grade()}")
        print(f"  • Status      : {new_student.get_status()}")
        return True
    else:
        print(f"\n [!] {msg}")
        return False


def handle_view_all_students(manager: ResultManager):
    print_header("All Enrolled Students")
    students = manager.get_all_students()

    if not students:
        print(" No students registered yet. Choose Option 1 to add a student.")
        return

    print(f"{'ID':<10} | {'Name':<18} | {'Total':<7} | {'Avg %':<7} | {'Grade':<6} | {'Status':<7}")
    print("-" * 72)

    for s in students:
        status_colored = f"\033[92m{s.get_status():<7}\033[0m" if s.get_status() == "Pass" else f"\033[91m{s.get_status():<7}\033[0m"
        print(f"{s.student_id:<10} | {s.name[:18]:<18} | {s.calculate_total():>7.2f} | {s.calculate_average():>6.2f}% | {s.calculate_grade():^6} | {status_colored}")

    print("-" * 72)
    print(f" Total Registered Students: {len(students)}")


def handle_search_student(manager: ResultManager):
    print_header("Search Student by ID")
    if manager.get_total_count() == 0:
        print(" [!] No student records found in memory. Please add students first.")
        return

    s_id = get_non_empty_input(" Enter Student ID to search: ")
    student = manager.search_student(s_id)

    if student:
        print(f"\n [✓] Student found!")
        display_student_card(student)
    else:
        print(f"\n [!] No student found with ID '{s_id}'.")


def handle_highest_lowest(manager: ResultManager):
    print_header("Top & Lowest Performing Students")

    if manager.get_total_count() == 0:
        print(" [!] No student records available.")
        return

    highest = manager.get_highest_scorer()
    lowest = manager.get_lowest_scorer()

    print("\n ★ HIGHEST SCORING STUDENT ★")
    display_student_card(highest)

    print("\n ▼ LOWEST SCORING STUDENT ▼")
    display_student_card(lowest)


def handle_class_summary(manager: ResultManager):
    print_header("Class Performance Summary")

    summary = manager.generate_class_summary()
    if not summary:
        print(" [!] No data available to generate a summary.")
        return

    print(f" Total Enrolled Students : {summary['total_students']}")
    print(f" Total Passed            : {summary['passed_count']} ({summary['pass_rate']}%)")
    print(f" Total Failed            : {summary['failed_count']} ({summary['fail_rate']}%)")
    print(f" Class Average Total     : {summary['class_avg_total']} / 500.0")
    print(f" Class Average Percentage: {summary['class_avg_percentage']}%")

    print_divider()
    print(" Grade Distribution:")
    for grade, count in summary['grade_distribution'].items():
        bar = "█" * count
        print(f"   Grade {grade:<3}: {count:>2} student(s)  {bar}")

    print_divider()
    print(" Subject-Wise Performance:")
    print(f"   {'Subject':<16} | {'Class Avg':<10} | {'Highest':<10} | {'Lowest':<10}")
    print("   " + "-" * 54)
    for subj, stats in summary['subject_stats'].items():
        print(f"   {subj:<16} | {stats['average']:>9.2f}  | {stats['highest']:>9.2f}  | {stats['lowest']:>9.2f}")

    print_divider()
    h = summary['highest_student']
    l = summary['lowest_student']
    print(f" Top Performer   : {h.name} (ID: {h.student_id}) - {h.calculate_total()} marks ({h.calculate_percentage()}%)")
    print(f" Lowest Performer: {l.name} (ID: {l.student_id}) - {l.calculate_total()} marks ({l.calculate_percentage()}%)")
    print_divider()


def handle_save_csv(manager: ResultManager):
    print_header("Save Records to CSV")
    if manager.get_total_count() == 0:
        print(" [!] No student records to save.")
        return

    filepath = input(f" Enter filename to save (press Enter for default '{manager.csv_filepath}'): ").strip()
    target = filepath if filepath else manager.csv_filepath

    success, msg = manager.save_to_csv(target)
    if success:
        print(f" [✓] {msg}")
    else:
        print(f" [!] {msg}")


def handle_load_csv(manager: ResultManager):
    print_header("Load Records from CSV")
    filepath = input(f" Enter filename to load (press Enter for default '{manager.csv_filepath}'): ").strip()
    target = filepath if filepath else manager.csv_filepath

    success, msg = manager.load_from_csv(target)
    if success:
        print(f" [✓] {msg}")
    else:
        print(f" [!] {msg}")


def display_menu():
    print("\n" + "=" * 72)
    print("      COACHING CENTER - STUDENT RESULT MANAGEMENT SYSTEM        ")
    print("=" * 72)
    print(" [1] Add New Student")
    print(" [2] View All Students")
    print(" [3] Search Student by ID")
    print(" [4] Display Highest & Lowest Scoring Students")
    print(" [5] Generate Class Performance Summary")
    print(" [6] Save Student Records to CSV ")
    print(" [7] Load Student Records from CSV")
    print(" [8] Exit Application")
    print("=" * 72)


def main():
    if sys.platform.startswith("win"):
        os.system("")

    manager = ResultManager()
    has_unsaved_changes = False

    default_csv = manager.csv_filepath
    if os.path.exists(default_csv):
        print(f"\n [i] Found existing database '{default_csv}'.")
        auto_load = input(" Would you like to load existing records? (Y/n): ").strip().lower()
        if auto_load in ('', 'y', 'yes'):
            success, msg = manager.load_from_csv(default_csv)
            print(f" [✓] {msg}")

    while True:
        display_menu()
        choice = input(" Select an option (1-8): ").strip()

        if choice == "1":
            if handle_add_student(manager):
                has_unsaved_changes = True
        elif choice == "2":
            handle_view_all_students(manager)
        elif choice == "3":
            handle_search_student(manager)
        elif choice == "4":
            handle_highest_lowest(manager)
        elif choice == "5":
            handle_class_summary(manager)
        elif choice == "6":
            handle_save_csv(manager)
            has_unsaved_changes = False
        elif choice == "7":
            handle_load_csv(manager)
        elif choice == "8":
            if has_unsaved_changes and manager.get_total_count() > 0:
                save_prompt = input("\n [?] You have unsaved changes. Save before exit? (Y/n): ").strip().lower()
                if save_prompt in ('', 'y', 'yes'):
                    manager.save_to_csv()
                    print(" [✓] Records saved successfully.")
            print("\n Thank you for using Coaching Center Result Manager. Goodbye!\n")
            break
        else:
            print("\n [!] Invalid selection! Please enter a number between 1 and 8.")

        input("\n Press Enter to return to main menu...")


if __name__ == "__main__":
    main()
