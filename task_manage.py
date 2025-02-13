import sqlite3
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

# Abstract base class for task views
class TaskView(ABC):
    """
    Abstract base class that defines the interface for task views.
    Subclasses must implement the display method to show tasks in a specific way.
    """
    @abstractmethod
    def display(self, tasks: list) -> None:
        """
        Display tasks.

        Args:
            tasks (list): List of tasks to display.
        """
        pass

# View tasks by deadline
class DeadlineView(TaskView):
    """
    View for displaying tasks sorted by deadline.
    """
    def display(self, tasks: list) -> None:
        """
        Display tasks sorted by deadline.

        Args:
            tasks (list): List of tasks to display.
        """
        print("Tasks sorted by Deadline:")
        for task in tasks:
            print(f"ID: {task[0]}, Description: {task[1]}, Deadline: {task[2]}, Status: {task[3]}, Priority: {task[4]}")

# View tasks by priority
class PriorityView(TaskView):
    """
    View for displaying tasks sorted by priority.
    """
    def display(self, tasks: list) -> None:
        """
        Display tasks sorted by priority.

        Args:
            tasks (list): List of tasks to display.
        """
        print("Tasks sorted by Priority:")
        for task in tasks:
            print(f"ID: {task[0]}, Description: {task[1]}, Deadline: {task[2]}, Status: {task[3]}, Priority: {task[4]}")

# TaskManager class with polymorphism and error handling
class TaskManager:
    """
    Task Manager class that allows adding, viewing, updating, deleting, filtering, 
    and searching tasks stored in an SQLite database.
    """
    def __init__(self, db_name: str = "tasks.db") -> None:
        """
        Initialize TaskManager with a database name and initialize the database.

        Args:
            db_name (str): The name of the SQLite database.
        """
        self.__db_name = db_name
        self.__init_db()

    def __init_db(self) -> None:
        """
        Initialize the database by creating the tasks table if it doesn't exist.
        """
        conn = sqlite3.connect(self.__db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                deadline TEXT,
                status TEXT CHECK(status IN ('Pending', 'Completed')) NOT NULL DEFAULT 'Pending',
                priority TEXT CHECK(priority IN ('high', 'medium', 'low')) DEFAULT 'medium'
            )
        ''')
        conn.commit()
        conn.close()

    def __connect(self) -> sqlite3.Connection:
        """
        Connect to the SQLite database.

        Returns:
            sqlite3.Connection: A connection to the database.
        """
        return sqlite3.connect(self.__db_name)

    def add_task(self, description: str, deadline: str, priority: str = "medium", status: str = "Pending") -> None:
        """
        Add a new task to the database.

        Args:
            description (str): The description of the task.
            deadline (str): The deadline of the task.
            priority (str): The priority of the task (default: "medium").
            status (str): The status of the task (default: "Pending").
        """
        if not description:
            print("Task description cannot be empty.")
            return
        if priority not in ["high", "medium", "low"]:
            print("Invalid priority. Must be 'high', 'medium', or 'low'.")
            return
        if status not in ["Pending", "Completed"]:
            print("Invalid status. Must be 'Pending' or 'Completed'.")
            return
        
        conn = self.__connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (description, deadline, status, priority) VALUES (?, ?, ?, ?)", 
                       (description, deadline, status, priority))
        conn.commit()
        conn.close()
        print("Task added successfully!")

    def view_tasks(self, order_by: str = None) -> list:
        """
        View tasks, optionally sorted by a specified attribute.

        Args:
            order_by (str): Attribute to sort by ("deadline" or "priority").
        
        Returns:
            list: List of tasks from the database.
        """
        conn = self.__connect()
        cursor = conn.cursor()
        query = "SELECT * FROM tasks"
        if order_by == "deadline":
            query += " ORDER BY deadline"
        elif order_by == "priority":
            query += " ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 END"
        cursor.execute(query)
        tasks = cursor.fetchall()
        conn.close()
        if not tasks:
            print("No tasks available.")
        else:
            return tasks

    def update_task(self, task_ids: list, description: str = None, status: str = None, priority: str = None, deadline: str = None) -> None:
        """
        Update one or more tasks in the database.

        Args:
            task_ids (list): List of task IDs to update.
            description (str): New description for the task (optional).
            status (str): New status for the task (optional).
            priority (str): New priority for the task (optional).
            deadline (str): New deadline for the task (optional).
        """
        try:
            task_ids = [int(task_id) for task_id in task_ids]  # Ensure IDs are integers
        except ValueError:
            print("Invalid task IDs. Task IDs must be numbers.")
            return
        
        conn = self.__connect()
        cursor = conn.cursor()
        for task_id in task_ids:
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            task = cursor.fetchone()

            if not task:
                print(f"No task found with ID {task_id}. Skipping this ID.")
                continue
            
            if description:
                cursor.execute("UPDATE tasks SET description = ? WHERE id = ?", (description, task_id))
            
            if status:
                status = "Pending" if status == "1" else "Completed"
                cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
            
            if priority:
                cursor.execute("UPDATE tasks SET priority = ? WHERE id = ?", (priority, task_id))
            
            if deadline:
                cursor.execute("UPDATE tasks SET deadline = ? WHERE id = ?", (deadline, task_id))
        
        conn.commit()
        conn.close()
        print(f"Tasks with IDs {task_ids} updated successfully!")

    def delete_task(self, task_ids: list) -> None:
        """
        Delete one or more tasks from the database.

        Args:
            task_ids (list): List of task IDs to delete.
        """
        try:
            task_ids = [int(task_id) for task_id in task_ids]  # Ensure IDs are integers
        except ValueError:
            print("Invalid task IDs. Task IDs must be numbers.")
            return
        
        conn = self.__connect()
        cursor = conn.cursor()
        for task_id in task_ids:
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            task = cursor.fetchone()

            if not task:
                print(f"No task found with ID {task_id}. Skipping this ID.")
                continue
            
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        
        conn.commit()
        conn.close()
        print(f"Tasks with IDs {task_ids} deleted successfully!")

    def filter_tasks(self, status: str) -> None:
        """
        Filter tasks based on their status.

        Args:
            status (str): Status to filter by ("1" for Pending, "2" for Completed).
        """
        if status not in ["1", "2"]:
            print("Invalid status input. Please enter '1' for Pending or '2' for Completed.")
            return
        status = "Pending" if status == "1" else "Completed"
        conn = self.__connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE status = ?", (status,))
        tasks = cursor.fetchall()
        conn.close()
        if not tasks:
            print(f"No {status} tasks available.")
        else:
            for task in tasks:
                print(f"ID: {task[0]}, Description: {task[1]}, Deadline: {task[2]}, Status: {task[3]}, Priority: {task[4]}")

    def search_tasks(self, keyword: str) -> None:
        """
        Search for tasks based on a keyword in their description.

        Args:
            keyword (str): The keyword to search for in task descriptions.
        """
        if not keyword:
            print("Search keyword cannot be empty.")
            return
        conn = self.__connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE description LIKE ?", (f"%{keyword}%",))
        tasks = cursor.fetchall()
        conn.close()
        if not tasks:
            print("No matching tasks found.")
        else:
            for task in tasks:
                print(f"ID: {task[0]}, Description: {task[1]}, Deadline: {task[2]}, Status: {task[3]}, Priority: {task[4]}")

    def due_soon_tasks(self) -> None:
        """
        View tasks that are due within the next 24 hours and are still pending.
        """
        conn = self.__connect()
        cursor = conn.cursor()
        now = datetime.now()
        upcoming = (now + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("SELECT * FROM tasks WHERE deadline <= ? AND status = 'Pending'", (upcoming,))
        tasks = cursor.fetchall()
        conn.close()
        print(f"Checking for tasks due on or before: {upcoming}")

        if not tasks:
            print("No tasks due soon.")
        else:
            print("Tasks due soon:")
            for task in tasks:
                print(f"ID: {task[0]}, Description: {task[1]}, Deadline: {task[2]}, Status: {task[3]}, Priority: {task[4]}")

    def run(self) -> None:
        """
        Start the task manager program and provide the user with options to manage tasks.
        """
        while True:
            print("\nTask Manager")
            print("1. Add Task")
            print("2. View Tasks")
            print("3. Update Task")
            print("4. Delete Task")
            print("5. Filter Tasks")
            print("6. Search Tasks")
            print("7. View Due Soon Tasks")
            print("8. Exit")
            choice = input("Choose an option: ")
            
            if choice == "1":
                description = input("Enter task description: ")
                
                # Generate a list of upcoming dates
                today = datetime.now()
                dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
                
                print("Select a deadline:")
                for idx, date in enumerate(dates, 1):
                    print(f"{idx}. {date}")

                deadline_choice = input("Enter choice (1-7): ")
                if deadline_choice.isdigit() and 1 <= int(deadline_choice) <= 7:
                    deadline = dates[int(deadline_choice) - 1]
                else:
                    print("Invalid choice, setting deadline as today.")
                    deadline = dates[0]

                print("Select priority:")
                print("1. High")
                print("2. Low")
                print("3. Medium")
                priority_choice = input("Enter choice (1-3): ")
                if priority_choice == "1":
                    priority = "high"
                elif priority_choice == "2":
                    priority = "low"
                elif priority_choice == "3":
                    priority = "medium"
                else:
                    print("Invalid priority choice, setting to medium.")
                    priority = "medium"
                
                self.add_task(description, deadline, priority)
            elif choice == "2":
                print("Sort tasks by:")
                print("1. Deadline")
                print("2. Priority")
                order_by = input("Enter choice (1 for Deadline, 2 for Priority): ")
                if order_by == "1":
                    tasks = self.view_tasks(order_by="deadline")
                    view = DeadlineView()
                elif order_by == "2":
                    tasks = self.view_tasks(order_by="priority")
                    view = PriorityView()
                else:
                    print("Invalid choice. Showing tasks by deadline by default.")
                    tasks = self.view_tasks(order_by="deadline")
                    view = DeadlineView()
                view.display(tasks)
            elif choice == "3":
                task_ids = input("Enter task IDs to update: ").split(",")
                description = input("Enter new description(leave blank to keep unchanged): ")
                status = input("Enter new status (1 for Pending, 2 for Completed, leave blank to keep unchanged): ")
                priority = input("Enter new priority (1 for High, 2 for Low, 3 for Medium, leave blank to keep unchanged): ")

                # Generate a list of upcoming dates from today
                today = datetime.now()
                dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
                print("Select a new deadline:")
                for idx, date in enumerate(dates, 1):
                    print(f"{idx}. {date}")

                deadline_choice = input("Enter choice (1-7): ")
                if deadline_choice.isdigit() and 1 <= int(deadline_choice) <= 7:
                    deadline = dates[int(deadline_choice) - 1]
                else:
                    print("Invalid choice, keeping existing deadline.")
                    deadline = None

                self.update_task(task_ids, description, status, priority, deadline)
            elif choice == "4":
                task_ids = input("Enter task IDs to delete: ").split(",")
                self.delete_task(task_ids)
            elif choice == "5":
                status = input("Enter task status to filter (1 for Pending, 2 for Completed): ")
                self.filter_tasks(status)
            elif choice == "6":
                keyword = input("Enter search keyword: ")
                self.search_tasks(keyword)
            elif choice == "7":
                self.due_soon_tasks()
            elif choice == "8":
                print("Exiting Task Manager.")
                break
            else:
                print("Invalid choice. Please try again.")



if __name__ == "__main__":
    manager = TaskManager()
    manager.run()
