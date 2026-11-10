import os
import unittest
from student import Student
from result_manager import ResultManager


class TestStudentModel(unittest.TestCase):
    def setUp(self):
        self.marks = {
            "Math": 85.0,
            "Science": 90.0,
            "English": 75.0,
            "History": 80.0,
            "Computer": 95.0
        }
        self.student = Student("S101", "Rahim Uddin", self.marks)

    def test_calculations(self):
        self.assertEqual(self.student.calculate_total(), 425.0)
        self.assertEqual(self.student.calculate_average(), 85.0)
        self.assertEqual(self.student.calculate_percentage(), 85.0)
        self.assertEqual(self.student.calculate_grade(), "A")
        self.assertEqual(self.student.get_status(), "Pass")

    def test_invalid_marks(self):
        s = Student("S102", "Invalid Mark Tester")
        with self.assertRaises(ValueError):
            s.set_mark("Math", -5)
        with self.assertRaises(ValueError):
            s.set_mark("Science", 105)
        with self.assertRaises(ValueError):
            s.set_mark("English", "abc")

    def test_fail_status_on_single_subject(self):
        failing_marks = {
            "Math": 35.0,
            "Science": 90.0,
            "English": 85.0,
            "History": 80.0,
            "Computer": 90.0
        }
        failing_student = Student("S103", "Karim Ali", failing_marks)
        self.assertEqual(failing_student.get_status(), "Fail")
        self.assertEqual(failing_student.calculate_grade(), "F")
        self.assertIn("Math", failing_student.get_failed_subjects())

    def test_grade_boundaries(self):
        def make_student(pct):
            marks = {subj: pct for subj in Student.DEFAULT_SUBJECTS}
            return Student("T1", "Tester", marks)

        self.assertEqual(make_student(95).calculate_grade(), "A+")
        self.assertEqual(make_student(90).calculate_grade(), "A+")
        self.assertEqual(make_student(85).calculate_grade(), "A")
        self.assertEqual(make_student(80).calculate_grade(), "A")
        self.assertEqual(make_student(75).calculate_grade(), "B")
        self.assertEqual(make_student(65).calculate_grade(), "C")
        self.assertEqual(make_student(55).calculate_grade(), "D")
        self.assertEqual(make_student(45).calculate_grade(), "E")
        self.assertEqual(make_student(35).calculate_grade(), "F")


class TestResultManager(unittest.TestCase):
    def setUp(self):
        self.test_csv = "test_students_temp.csv"
        self.manager = ResultManager(csv_filepath=self.test_csv)

        self.s1 = Student("S101", "Rahim", {"Math": 85, "Science": 90, "English": 80, "History": 75, "Computer": 95})
        self.s2 = Student("S102", "Karim", {"Math": 95, "Science": 98, "English": 92, "History": 88, "Computer": 99})
        self.s3 = Student("S103", "Ayesha", {"Math": 30, "Science": 45, "English": 50, "History": 40, "Computer": 55})

        self.manager.add_student(self.s1)
        self.manager.add_student(self.s2)
        self.manager.add_student(self.s3)

    def tearDown(self):
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)

    def test_duplicate_prevention(self):
        dup = Student("S101", "Rahim Duplicate", {"Math": 50, "Science": 50, "English": 50, "History": 50, "Computer": 50})
        success, msg = self.manager.add_student(dup)
        self.assertFalse(success)
        self.assertIn("already exists", msg)

    def test_search_student(self):
        res = self.manager.search_student("s102")
        self.assertIsNotNone(res)
        self.assertEqual(res.name, "Karim")

        not_found = self.manager.search_student("NONEXISTENT")
        self.assertIsNone(not_found)

    def test_highest_and_lowest_scorer(self):
        highest = self.manager.get_highest_scorer()
        lowest = self.manager.get_lowest_scorer()

        self.assertEqual(highest.student_id, "S102")
        self.assertEqual(highest.calculate_total(), 472.0)

        self.assertEqual(lowest.student_id, "S103")
        self.assertEqual(lowest.calculate_total(), 220.0)

    def test_class_summary(self):
        summary = self.manager.generate_class_summary()
        self.assertIsNotNone(summary)
        self.assertEqual(summary["total_students"], 3)
        self.assertEqual(summary["passed_count"], 2)
        self.assertEqual(summary["failed_count"], 1)
        self.assertAlmostEqual(summary["pass_rate"], 66.67, delta=0.01)
        self.assertEqual(summary["highest_student"].name, "Karim")
        self.assertEqual(summary["lowest_student"].name, "Ayesha")

    def test_csv_save_and_load(self):
        save_success, save_msg = self.manager.save_to_csv()
        self.assertTrue(save_success)
        self.assertTrue(os.path.exists(self.test_csv))

        new_manager = ResultManager(csv_filepath=self.test_csv)
        self.assertEqual(new_manager.get_total_count(), 0)

        load_success, load_msg = new_manager.load_from_csv()
        self.assertTrue(load_success)
        self.assertEqual(new_manager.get_total_count(), 3)

        loaded_s2 = new_manager.search_student("S102")
        self.assertIsNotNone(loaded_s2)
        self.assertEqual(loaded_s2.name, "Karim")
        self.assertEqual(loaded_s2.calculate_total(), 472.0)
        self.assertEqual(loaded_s2.calculate_grade(), "A+")


if __name__ == "__main__":
    unittest.main()
