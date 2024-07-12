class Student:
    def __init__(self, name):
        self.name = name
        self.scores = []

    def add_score(self, score):
        self.scores.append(score)

    def get_average(self):
        if len(self.scores) == 0:
            return 0
        return sum(self.scores) / len(self.scores)

class ScoreSystem:
    def __init__(self):
        self.students = {}

    def add_student(self, name):
        if name not in self.students:
            self.students[name] = Student(name)
            print(f"Student {name} added.")
        else:
            print(f"Student {name} already exists.")

    def record_score(self, name, score):
        if name in self.students:
            self.students[name].add_score(score)
            print(f"Score {score} recorded for {name}.")
        else:
            print(f"Student {name} not found.")

    def get_student_average(self, name):
        if name in self.students:
            avg = self.students[name].get_average()
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

def main():
    system = ScoreSystem()
    
    while True:
        print("\nSchool Score Recording System")
        print("1. Add a student")
        print("2. Record a score")
        print("3. Get a student's average score")
        print("4. Get all students' average scores")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            name = input("Enter student name: ")
            system.add_student(name)
        elif choice == '2':
            name = input("Enter student name: ")
            score = float(input("Enter score: "))
            system.record_score(name, score)
        elif choice == '3':
            name = input("Enter student name: ")
            system.get_student_average(name)
        elif choice == '4':
            system.get_all_averages()
        elif choice == '5':
            print("Thank you for using the School Score Recording System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()