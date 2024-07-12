import sys
import json
import os
from typing import Dict, List, Optional
from decimal import Decimal, InvalidOperation

class Score:
    def __init__(self, subject: str, value: Decimal):
        self.subject = subject.lower()
        self.value = value

    def to_dict(self) -> Dict:
        return {"subject": self.subject, "value": str(self.value)}

    @classmethod
    def from_dict(cls, data: Dict) -> 'Score':
        return cls(data["subject"], Decimal(data["value"]))

class Student:
    def __init__(self, name: str):
        self.name = name
        self.scores: List[Score] = []

    def add_score(self, subject: str, value: Decimal) -> None:
        self.scores.append(Score(subject, value))

    def remove_score(self, index: int) -> bool:
        if 0 <= index < len(self.scores):
            del self.scores[index]
            return True
        return False

    def get_average(self, subject: Optional[str] = None) -> Decimal:
        relevant_scores = [score.value for score in self.scores if subject is None or score.subject == subject.lower()]
        return sum(relevant_scores) / len(relevant_scores) if relevant_scores else Decimal('0')

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "scores": [score.to_dict() for score in self.scores]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Student':
        student = cls(data["name"])
        student.scores = [Score.from_dict(score_data) for score_data in data["scores"]]
        return student

class ScoreSystem:
    def __init__(self):
        self.students: Dict[str, Student] = {}
        self.subjects: set = set()
        self.load_data()

    def add_student(self, name: str) -> None:
        name = name.strip()
        if not name:
            print("Error: Student name cannot be empty.")
            return
        if name in self.students:
            print(f"Error: Student {name} already exists.")
        else:
            self.students[name] = Student(name)
            print(f"Student {name} added successfully.")
            self.save_data()

    def remove_student(self, name: str) -> None:
        if name in self.students:
            confirmation = input(f"Are you sure you want to remove {name}? (y/n): ").lower()
            if confirmation == 'y':
                del self.students[name]
                print(f"Student {name} removed successfully.")
                self.save_data()
            else:
                print("Operation cancelled.")
        else:
            print(f"Error: Student {name} not found.")

    def record_score(self, name: str, subject: str, score: str) -> None:
        if name not in self.students:
            print(f"Error: Student {name} not found.")
            return
        try:
            score_value = Decimal(score).quantize(Decimal('0.01'))
            if Decimal('0') <= score_value <= Decimal('100'):
                subject = subject.lower()
                self.students[name].add_score(subject, score_value)
                self.subjects.add(subject)
                print(f"Score {score_value} recorded for {name} in {subject}.")
                self.save_data()
            else:
                print("Error: Score must be between 0 and 100.")
        except InvalidOperation:
            print("Error: Invalid score. Please enter a number.")

    def remove_score(self, name: str, index: int) -> None:
        if name not in self.students:
            print(f"Error: Student {name} not found.")
            return
        if self.students[name].remove_score(index):
            print(f"Score removed for {name}.")
            self.save_data()
        else:
            print("Error: Invalid score index.")

    def get_student_average(self, name: str, subject: Optional[str] = None) -> None:
        student = self.students.get(name)
        if student:
            avg = student.get_average(subject)
            subject_str = f" in {subject}" if subject else ""
            print(f"{name}'s average score{subject_str}: {avg:.2f}")
        else:
            print(f"Error: Student {name} not found.")

    def get_all_averages(self, subject: Optional[str] = None) -> None:
        if not self.students:
            print("No students in the system.")
        else:
            subject_str = f" in {subject}" if subject else ""
            for name, student in self.students.items():
                avg = student.get_average(subject)
                print(f"{name}'s average score{subject_str}: {avg:.2f}")

    def list_students(self) -> None:
        if not self.students:
            print("No students in the system.")
        else:
            for name in self.students:
                print(name)

    def view_student_scores(self, name: str) -> None:
        student = self.students.get(name)
        if student:
            if student.scores:
                for i, score in enumerate(student.scores):
                    print(f"{i+1}. {score.subject}: {score.value}")
            else:
                print(f"{name} has no recorded scores.")
        else:
            print(f"Error: Student {name} not found.")

    def save_data(self) -> None:
        data = {
            "students": {name: student.to_dict() for name, student in self.students.items()},
            "subjects": list(self.subjects)
        }
        try:
            with open("school_data.json", "w") as f:
                json.dump(data, f, indent=2)
        except IOError:
            print("Error: Unable to save data. Please check file permissions.")

    def load_data(self) -> None:
        if os.path.exists("school_data.json"):
            try:
                with open("school_data.json", "r") as f:
                    data = json.load(f)
                self.students = {name: Student.from_dict(student_data) for name, student_data in data["students"].items()}
                self.subjects = set(data.get("subjects", []))
            except (IOError, json.JSONDecodeError):
                print("Error: Unable to load data. Starting with an empty system.")
                self.students = {}
                self.subjects = set()

def get_input(prompt: str) -> str:
    return input(prompt).strip()

def get_numeric_input(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def display_menu() -> None:
    print("\nSchool Score Recording System")
    print("1. Add a student")
    print("2. Remove a student")
    print("3. Record a score")
    print("4. Remove a score")
    print("5. Get a student's average score")
    print("6. Get all students' average scores")
    print("7. List all students")
    print("8. View a student's scores")
    print("9. List all subjects")
    print("10. Exit")

def handle_choice(system: ScoreSystem, choice: int) -> None:
    if choice == 1:
        name = get_input("Enter student name: ")
        system.add_student(name)
    elif choice == 2:
        name = get_input("Enter student name: ")
        system.remove_student(name)
    elif choice == 3:
        name = get_input("Enter student name: ")
        subject = get_input("Enter subject: ")
        score = get_input("Enter score: ")
        system.record_score(name, subject, score)
    elif choice == 4:
        name = get_input("Enter student name: ")
        system.view_student_scores(name)
        index = get_numeric_input("Enter the index of the score to remove: ") - 1
        system.remove_score(name, index)
    elif choice == 5:
        name = get_input("Enter student name: ")
        subject = get_input("Enter subject (or press Enter for overall average): ")
        system.get_student_average(name, subject if subject else None)
    elif choice == 6:
        subject = get_input("Enter subject (or press Enter for overall average): ")
        system.get_all_averages(subject if subject else None)
    elif choice == 7:
        system.list_students()
    elif choice == 8:
        name = get_input("Enter student name: ")
        system.view_student_scores(name)
    elif choice == 9:
        print("Subjects:", ", ".join(sorted(system.subjects)) if system.subjects else "No subjects recorded yet.")
    elif choice == 10:
        print("Thank you for using the School Score Recording System. Goodbye!")
        sys.exit(0)
    else:
        print("Invalid choice. Please enter a number between 1 and 10.")

def main() -> None:
    system = ScoreSystem()
    
    while True:
        display_menu()
        choice = get_numeric_input("Enter your choice (1-10): ")
        handle_choice(system, choice)

if __name__ == "__main__":
    main()