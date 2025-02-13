# task_management
1. How to run the program.
    Clone the repository from GitHub
    Navigate to the project folder
    Run the program using Python 3 python3 task_manage.py

2. Additional Features

    a. polymorphism - The program uses an abstract base class (TaskView) for different views like DeadlineView and PriorityView. This allows dynamic task display based on user input.

    b.  Encapsulation

        Data encapsulation: The TaskManager class encapsulates the database connection details and task management logic. The database name (__db_name) and connection method (__connect) are private, preventing direct access from outside the class.

        Function encapsulation: Task-related operations (add, update, delete, view tasks) are wrapped inside the TaskManager class, which helps in grouping these operations logically and makes the code more organized and modular.

3. Add, update, delete, and view tasks.

4. Sort tasks by deadline or priority.

5. Filter and search tasks by status or description.

6. View tasks due soon (within 24 hours).

7. Libraries Used:

    datetime and timedelta for deadline calculations.
    ABC for polymorphism.
    SQLite for database storage.
