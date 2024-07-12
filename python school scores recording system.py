import sys

class Student:
    def __init__(self, name):
        self.name = name
        self.scores = []

    def add_score(self, score):
        self.scores.append(score)

    def get_average(self):
        return sum(self.scores) / len(self.scores) if self.scores else 0

class ScoreSystem:
    def __init__(self):
        self.students = {}

    def add_student(self, name):
        if not name.strip():
            print("Student name cannot be empty.")
            return
        if name in self.students:
            print(f"Student {name} already exists.")
        else:
            self.students[name] = Student(name)
            print(f"Student {name} added.")

    def record_score(self, name, score):
        if name not in self.students:
            print(f"Student {name} not found.")
            return
        try:
            score = float(score)
            if 0 <= score <= 100:
                self.students[name].add_score(score)
                print(f"Score {score} recorded for {name}.")
            else:
                print("Score must be between 0 and 100.")
        except ValueError:
            print("Invalid score. Please enter a number.")

    def get_student_average(self, name):
        student = self.students.get(name)
        if student:
            avg = student.get_average()
            print(f"{name}'s average score: {avg:.2f}")
        else:
            print(f"Student {name} not found.")

    def get_all_averages(self):
        if not self.students:
            print("No students in the system.")
        else:
            for name, student in self.students.items():
                avg = student.get_average()
                print(f"{name}'s average score: {avg:.2f}")

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
                print(f"{name}'s scores: {', '.join(map(str, student.scores))}")
            else:
                print(f"{name} has no recorded scores.")
        else:
            print(f"Student {name} not found.")

def get_input(prompt):
    return input(prompt).strip()

def main():
    system = ScoreSystem()
    
    while True:
        print("\nSchool Score Recording System")
        print("1. Add a student")
        print("2. Record a score")
        print("3. Get a student's average score")
        print("4. Get all students' average scores")
        print("5. List all students")
        print("6. View a student's scores")
        print("7. Exit")
        
        try:
            choice = int(get_input("Enter your choice (1-7): "))
            
            if choice == 1:
                name = get_input("Enter student name: ")
                system.add_student(name)
            elif choice == 2:
                name = get_input("Enter student name: ")
                score = get_input("Enter score: ")
                system.record_score(name, score)
            elif choice == 3:
                name = get_input("Enter student name: ")
                system.get_student_average(name)
            elif choice == 4:
                system.get_all_averages()
            elif choice == 5:
                system.list_students()
            elif choice == 6:
                name = get_input("Enter student name: ")
                system.view_student_scores(name)
            elif choice == 7:
                print("Thank you for using the School Score Recording System. Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()