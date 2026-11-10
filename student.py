class Student:
    DEFAULT_SUBJECTS = ["Math", "Science", "English", "History", "Computer"]
    PASSING_THRESHOLD = 40.0

    def __init__(self, student_id: str, name: str, marks: dict = None):
        self.student_id = str(student_id).strip()
        self.name = str(name).strip()
        self.marks = {}

        if marks:
            for subject, mark in marks.items():
                self.set_mark(subject, mark)

    def set_mark(self, subject: str, mark: float):
        try:
            val = float(mark)
        except (ValueError, TypeError):
            raise ValueError(f"Mark for {subject} must be a valid number.")

        if val < 0 or val > 100:
            raise ValueError(f"Mark for {subject} must be between 0 and 100 (got {val}).")

        self.marks[subject.strip()] = round(val, 2)

    def calculate_total(self) -> float:
        return round(sum(self.marks.values()), 2)

    def calculate_average(self) -> float:
        if not self.marks:
            return 0.0
        return round(self.calculate_total() / len(self.marks), 2)

    def calculate_percentage(self) -> float:
        if not self.marks:
            return 0.0
        max_marks = len(self.marks) * 100.0
        return round((self.calculate_total() / max_marks) * 100.0, 2)

    def calculate_grade(self) -> str:
        if self.get_status() == "Fail":
            return "F"

        pct = self.calculate_percentage()
        if pct >= 90:
            return "A+"
        elif pct >= 80:
            return "A"
        elif pct >= 70:
            return "B"
        elif pct >= 60:
            return "C"
        elif pct >= 50:
            return "D"
        elif pct >= 40:
            return "E"
        else:
            return "F"

    def get_failed_subjects(self) -> list:
        return [subj for subj, mark in self.marks.items() if mark < self.PASSING_THRESHOLD]

    def get_status(self) -> str:
        if not self.marks:
            return "Fail"

        if len(self.get_failed_subjects()) > 0:
            return "Fail"

        if self.calculate_percentage() < self.PASSING_THRESHOLD:
            return "Fail"

        return "Pass"

    def to_dict(self) -> dict:
        data = {
            "student_id": self.student_id,
            "name": self.name,
            "total": self.calculate_total(),
            "average": self.calculate_average(),
            "percentage": self.calculate_percentage(),
            "grade": self.calculate_grade(),
            "status": self.get_status()
        }
        for subj, mark in self.marks.items():
            data[subj] = mark
        return data

    @classmethod
    def from_dict(cls, data: dict, subject_keys: list = None):
        student_id = data.get("student_id", "")
        name = data.get("name", "")
        subjects = subject_keys or cls.DEFAULT_SUBJECTS

        marks = {}
        for subj in subjects:
            if subj in data and data[subj] != "":
                marks[subj] = float(data[subj])

        return cls(student_id=student_id, name=name, marks=marks)

    def __str__(self) -> str:
        marks_str = ", ".join(f"{subj}: {mark}" for subj, mark in self.marks.items())
        return (
            f"ID: {self.student_id} | Name: {self.name} | "
            f"Marks: [{marks_str}] | Total: {self.calculate_total()} | "
            f"Avg: {self.calculate_average()}% | Grade: {self.calculate_grade()} | "
            f"Status: {self.get_status()}"
        )
