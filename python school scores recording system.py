import sys
import json
import os
import csv
from typing import Dict, List, Optional
from decimal import Decimal, InvalidOperation
import statistics
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog

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
            raise ValueError("Student name cannot be empty.")
        if name in self.students:
            raise ValueError(f"Student {name} already exists.")
        self.students[name] = Student(name)
        self.save_data()

    def remove_student(self, name: str) -> None:
        if name not in self.students:
            raise ValueError(f"Student {name} not found.")
        del self.students[name]
        self.save_data()

    def record_score(self, name: str, subject: str, score: str) -> None:
        if name not in self.students:
            raise ValueError(f"Student {name} not found.")
        try:
            score_value = Decimal(score).quantize(Decimal('0.01'))
            if not (Decimal('0') <= score_value <= Decimal('100')):
                raise ValueError("Score must be between 0 and 100.")
            subject = subject.lower()
            self.students[name].add_score(subject, score_value)
            self.subjects.add(subject)
            self.save_data()
        except InvalidOperation:
            raise ValueError("Invalid score. Please enter a number.")

    def remove_score(self, name: str, index: int) -> None:
        if name not in self.students:
            raise ValueError(f"Student {name} not found.")
        if not self.students[name].remove_score(index):
            raise ValueError("Invalid score index.")
        self.save_data()

    def get_student_average(self, name: str, subject: Optional[str] = None) -> Decimal:
        student = self.students.get(name)
        if not student:
            raise ValueError(f"Student {name} not found.")
        return student.get_average(subject)

    def get_all_averages(self, subject: Optional[str] = None) -> Dict[str, Decimal]:
        return {name: student.get_average(subject) for name, student in self.students.items()}

    def get_statistics(self, subject: Optional[str] = None) -> Dict[str, Decimal]:
        scores = [score.value for student in self.students.values() for score in student.scores 
                  if subject is None or score.subject == subject]
        if not scores:
            return {"count": 0, "mean": Decimal('0'), "median": Decimal('0'), "mode": Decimal('0'), 
                    "std_dev": Decimal('0'), "min": Decimal('0'), "max": Decimal('0')}
        return {
            "count": len(scores),
            "mean": Decimal(str(statistics.mean(scores))),
            "median": Decimal(str(statistics.median(scores))),
            "mode": Decimal(str(statistics.mode(scores))),
            "std_dev": Decimal(str(statistics.stdev(scores))) if len(scores) > 1 else Decimal('0'),
            "min": min(scores),
            "max": max(scores)
        }

    def export_to_csv(self, filename: str) -> None:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Student', 'Subject', 'Score'])
            for student in self.students.values():
                for score in student.scores:
                    writer.writerow([student.name, score.subject, score.value])

    def save_data(self) -> None:
        data = {
            "students": {name: student.to_dict() for name, student in self.students.items()},
            "subjects": list(self.subjects)
        }
        with open("school_data.json", "w") as f:
            json.dump(data, f, indent=2)

    def load_data(self) -> None:
        if os.path.exists("school_data.json"):
            with open("school_data.json", "r") as f:
                data = json.load(f)
            self.students = {name: Student.from_dict(student_data) for name, student_data in data["students"].items()}
            self.subjects = set(data.get("subjects", []))

class ScoreSystemGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("School Score Recording System")
        self.system = ScoreSystem()

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.create_students_tab()
        self.create_scores_tab()
        self.create_statistics_tab()

    def create_students_tab(self):
        students_frame = ttk.Frame(self.notebook)
        self.notebook.add(students_frame, text="Students")

        ttk.Button(students_frame, text="Add Student", command=self.add_student).pack(pady=5)
        ttk.Button(students_frame, text="Remove Student", command=self.remove_student).pack(pady=5)

        self.students_listbox = tk.Listbox(students_frame)
        self.students_listbox.pack(pady=5, fill=tk.BOTH, expand=True)
        self.update_students_list()

    def create_scores_tab(self):
        scores_frame = ttk.Frame(self.notebook)
        self.notebook.add(scores_frame, text="Scores")

        ttk.Button(scores_frame, text="Add Score", command=self.add_score).pack(pady=5)
        ttk.Button(scores_frame, text="Remove Score", command=self.remove_score).pack(pady=5)
        ttk.Button(scores_frame, text="View Scores", command=self.view_scores).pack(pady=5)
        ttk.Button(scores_frame, text="Export to CSV", command=self.export_to_csv).pack(pady=5)

    def create_statistics_tab(self):
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="Statistics")

        ttk.Button(stats_frame, text="View Statistics", command=self.view_statistics).pack(pady=5)

        self.stats_text = tk.Text(stats_frame, height=10, width=50)
        self.stats_text.pack(pady=5, fill=tk.BOTH, expand=True)

    def add_student(self):
        name = simpledialog.askstring("Add Student", "Enter student name:")
        if name:
            try:
                self.system.add_student(name)
                self.update_students_list()
                messagebox.showinfo("Success", f"Student {name} added successfully.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def remove_student(self):
        selection = self.students_listbox.curselection()
        if selection:
            name = self.students_listbox.get(selection[0])
            if messagebox.askyesno("Confirm", f"Are you sure you want to remove {name}?"):
                try:
                    self.system.remove_student(name)
                    self.update_students_list()
                    messagebox.showinfo("Success", f"Student {name} removed successfully.")
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please select a student to remove.")

    def add_score(self):
        name = simpledialog.askstring("Add Score", "Enter student name:")
        if name:
            subject = simpledialog.askstring("Add Score", "Enter subject:")
            if subject:
                score = simpledialog.askstring("Add Score", "Enter score:")
                if score:
                    try:
                        self.system.record_score(name, subject, score)
                        messagebox.showinfo("Success", f"Score recorded for {name} in {subject}.")
                    except ValueError as e:
                        messagebox.showerror("Error", str(e))

    def remove_score(self):
        name = simpledialog.askstring("Remove Score", "Enter student name:")
        if name:
            try:
                scores = self.system.students[name].scores
                score_list = [f"{i+1}. {score.subject}: {score.value}" for i, score in enumerate(scores)]
                index = simpledialog.askinteger("Remove Score", f"Select score to remove for {name}:\n" + "\n".join(score_list))
                if index is not None:
                    self.system.remove_score(name, index - 1)
                    messagebox.showinfo("Success", f"Score removed for {name}.")
            except KeyError:
                messagebox.showerror("Error", f"Student {name} not found.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def view_scores(self):
        name = simpledialog.askstring("View Scores", "Enter student name:")
        if name:
            try:
                scores = self.system.students[name].scores
                score_list = [f"{score.subject}: {score.value}" for score in scores]
                messagebox.showinfo(f"Scores for {name}", "\n".join(score_list) if score_list else "No scores recorded.")
            except KeyError:
                messagebox.showerror("Error", f"Student {name} not found.")

    def export_to_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            self.system.export_to_csv(filename)
            messagebox.showinfo("Success", f"Data exported to {filename}")

    def view_statistics(self):
        subject = simpledialog.askstring("View Statistics", "Enter subject (or leave blank for overall statistics):")
        stats = self.system.get_statistics(subject)
        self.stats_text.delete('1.0', tk.END)
        self.stats_text.insert(tk.END, f"Statistics for {subject or 'all subjects'}:\n\n")
        for key, value in stats.items():
            self.stats_text.insert(tk.END, f"{key.capitalize()}: {value}\n")

    def update_students_list(self):
        self.students_listbox.delete(0, tk.END)
        for name in self.system.students:
            self.students_listbox.insert(tk.END, name)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ScoreSystemGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)