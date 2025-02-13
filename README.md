
# Task Management Program

## Overview
This program allows users to manage tasks efficiently by providing features like adding, updating, deleting, sorting, and filtering tasks. It also supports viewing tasks based on various criteria such as deadline, priority, or status. The program is built with Python and uses SQLite for database storage.

## Features
- **Add, Update, Delete, and View Tasks:** Easily manage tasks by performing basic CRUD operations.
- **Sort Tasks by Deadline or Priority:** Sort tasks based on urgency or priority level.
- **Filter and Search Tasks:** Filter tasks by status or description for quick access.
- **View Tasks Due Soon:** Identify tasks that are due within the next 24 hours.
- **Polymorphism:** Utilizes an abstract base class (`TaskView`) for dynamic task display based on user input (e.g., `DeadlineView`, `PriorityView`).
- **Encapsulation:** 
  - **Data Encapsulation:** TaskManager class encapsulates database connection details (`__db_name`, `__connect`) to protect direct access.
  - **Function Encapsulation:** Task-related operations like adding, updating, deleting, and viewing tasks are grouped in the TaskManager class, ensuring modular and organized code.

## Requirements
- Python 3.x
- SQLite (no additional installation required)
- datetime and timedelta modules (included in Python standard library)
- ABC (abstract base class module for polymorphism)

## Installation and Setup
1. Clone the repository from GitHub:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project folder:
   ```bash
   cd task_management
   ```
3. Run the program using Python 3:
   ```bash
   python3 task_manage.py
   ```

## Libraries Used
- `datetime` and `timedelta`: For deadline calculations and time-based functionality.
- `ABC`: To implement polymorphism and abstract base classes for different task views.
- `SQLite`: For task storage and retrieval in a local database.

## Usage
Once the program is running, you'll be able to:
- Add tasks
- Update existing tasks
- Delete tasks
- View tasks based on different criteria
- Sort tasks by deadline or priority
- Filter tasks by status or description

