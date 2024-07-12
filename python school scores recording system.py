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
        for name, student in self.students.items():
            avg = student.get_average()
            print(f"{name}'s average score: {avg:.2f}")

system = ScoreSystem()

system.add_student("Alice")
system.add_student("Bob")
system.add_student("Charlie")

system.record_score("Alice", 85)
system.record_score("Alice", 92)
system.record_score("Bob", 78)
system.record_score("Charlie", 95)

system.get_student_average("Alice")
system.get_all_averages()