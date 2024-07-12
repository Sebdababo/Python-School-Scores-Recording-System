import sys
import json
import os

class Score:
    def __init__(self, subject, value):
        self.subject = subject
        self.value = value

class Student:
    def __init__(self, name):
        self.name = name
        self.scores = []

    def add_score(self, subject, value):
        self.scores.append(Score(subject, value))

    def remove_score(self, index):
        if 0 <= index < len(self.scores):
            del self.scores[index]
            return True
        return False

    def get_average(self, subject=None):
        if subject:
            subject_scores = [score.value for score in self.scores if score.subject == subject]
            return sum(subject_scores) / len(subject_scores) if subject_scores else 0
        else:
            return sum(score.value for score in self.scores) / len(self.scores) if self.scores else 0

    def to_dict(self):
        return {
            "name": self.name,
            "scores": [{"subject": score.subject, "value": score.value} for score in self.scores]
        }

    @classmethod
    def from_dict(cls, data):
        student = cls(data["name"])
        for score_data in data["scores"]:
            student.add_score(score_data["subject"], score_data["value"])
        return student

class ScoreSystem:
    def __init__(self):
        self.students = {}
        self.load_data()

    def add_student(self, name):
        if not name.strip():
            print("Student name cannot be empty.")
            return
        if name in self.students:
            print(f"Student {name} already exists.")
        else:
            self.students[name] = Student(name)
            print(f"Student {name} added.")
            self.save_data()

    def remove_student(self, name):
        if name in self.students:
            del self.students[name]
            print(f"Student {name} removed.")
            self.save_data()
        else:
            print(f"Student {name} not found.")

    def record_score(self, name, subject, score):
        if name not in self.students:
            print(f"Student {name} not found.")
            return
        try:
            score = float(score)
            if 0 <= score <= 100:
                self.students[name].add_score(subject, score)
                print(f"Score {score} recorded for {name} in {subject}.")
                self.save_data()
            else:
                print("Score must be between 0 and 100.")
        except ValueError:
            print("Invalid score. Please enter a number.")

    def remove_score(self, name, index):
        if name not in self.students:
            print(f"Student {name} not found.")
            return
        if self.students[name].remove_score(index):
            print(f"Score removed for {name}.")
            self.save_data()
        else:
            print("Invalid score index.")

    def get_student_average(self, name, subject=None):
        student = self.students.get(name)
        if student:
            avg = student.get_average(subject)
            subject_str = f" in {subject}" if subject else ""
            print(f"{name}'s average score{subject_str}: {avg:.2f}")
        else:
            print(f"Student {name} not found.")

    def get_all_averages(self, subject=None):
        if not self.students:
            print("No students in the system.")
        else:
            subject_str = f" in {subject}" if subject else ""
            for name, student in self.students.items():
                avg = student.get_average(subject)
                print(f"{name}'s average score{subject_str}: {avg:.2f}")

    def list_students(self):
        if not self.students:
            print("No students in the system.")
        else:
            for name in self.students:
                print(name)

    def view_student_scores(self, name):
        student = self.students.get(name)
        if student:
            if student.scores:
                for i, score in enumerate(student.scores):
                    print(f"{i+1}. {score.subject}: {score.value}")
            else:
                print(f"{name} has no recorded scores.")
        else:
            print(f"Student {name} not found.")

    def save_data(self):
        data = {name: student.to_dict() for name, student in self.students.items()}
        with open("school_data.json", "w") as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists("school_data.json"):
            with open("school_data.json", "r") as f:
                data = json.load(f)
            self.students = {name: Student.from_dict(student_data) for name, student_data in data.items()}

def get_input(prompt):
    return input(prompt).strip()

def main():
    system = ScoreSystem()
    
    while True:
        print("\nSchool Score Recording System")
        print("1. Add a student")
        print("2. Remove a student")
        print("3. Record a score")
        print("4. Remove a score")
        print("5. Get a student's average score")
        print("6. Get all students' average scores")
        print("7. List all students")
        print("8. View a student's scores")
        print("9. Exit")
        
        try:
            choice = int(get_input("Enter your choice (1-9): "))
            
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
                index = int(get_input("Enter the index of the score to remove: ")) - 1
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
                print("Thank you for using the School Score Recording System. Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please enter a number between 1 and 9.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()