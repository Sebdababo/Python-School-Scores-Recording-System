# Python School Scores Recording System

## Description

The Python School Scores Recording System is a comprehensive tool designed to manage and analyze student scores efficiently. It allows users to add students, record and remove scores, calculate averages, view statistics, and export data to CSV format. This application is built using Python and the Tkinter library for the graphical user interface.

## Features

- Add and remove students
- Record and remove scores for different subjects
- Calculate average scores per student and per subject
- View comprehensive statistics including mean, median, mode, standard deviation, and more
- Export data to CSV format for easy sharing and analysis
- User-friendly graphical interface

## Installation

1. **Clone the repository:**
    ```
    git clone https://github.com/Sebdababo/Python-School-Scores-Recording-System.git
    cd Python-School-Scores-Recording-System
    ```

2. **Install the required libraries:**
    ```
    pip install -r requirements.txt
    ```

3. **Run the application:**
    ```
    python school_scores_system.py
    ```

## Usage

### GUI Interface

When you run the application, a graphical user interface (GUI) will appear with three main tabs: **Students**, **Scores**, and **Statistics**.

#### Students Tab

- **Add Student:** Click the "Add Student" button and enter the student's name.
- **Remove Student:** Select a student from the list and click "Remove Student."

#### Scores Tab

- **Add Score:** Click "Add Score," enter the student's name, subject, and score.
- **Remove Score:** Click "Remove Score," select the student and score to remove.
- **View Scores:** Click "View Scores," enter the student's name to see their scores.
- **Export to CSV:** Click "Export to CSV" to save all student scores to a CSV file.

#### Statistics Tab

- **View Statistics:** Click "View Statistics," enter the subject (optional) to view statistics like mean, median, mode, etc. Leave blank to view overall statistics.

### Command Line Interface (CLI)

You can also use the CLI if you prefer. Below are some sample commands:

- **Add Student:**
    ```python
    system.add_student('John Doe')
    ```

- **Record Score:**
    ```python
    system.record_score('John Doe', 'Math', '95.5')
    ```

- **Remove Score:**
    ```python
    system.remove_score('John Doe', 0)
    ```

- **Get Student Average:**
    ```python
    print(system.get_student_average('John Doe', 'Math'))
    ```

- **Get Statistics:**
    ```python
    print(system.get_statistics('Math'))
    ```

## Data Persistence

The system saves all data in a JSON file (`school_data.json`) to maintain persistence between sessions. It automatically loads data on startup and saves any changes made through the GUI or CLI.
