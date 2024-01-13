from datetime import datetime   #it is used to handle due dates for tasks.

# Memento Pattern
  # it is used to implement the Memento Pattern. It stores the state of the task list at a specific point in time.

class Memento:
    def __init__(self, state):
        self._state = state

    def get_state(self):
        return self._state


# Task Builder Pattern
  #It is used to construct a Task object with optional attributes like due date and tags. It follows the Builder Pattern.
class TaskBuilder:
    def __init__(self, description):
        self.task = Task(description)

    def set_due_date(self, due_date):
        self.task.set_due_date(due_date)
        return self

    def set_tags(self, tags):
        self.task.set_tags(tags)
        return self

    def build(self):
        return self.task


# Task class
  #It has all the methods for setting due date, tags, marking as completed/pending, and displaying task details.    
class Task:
    def __init__(self, description):
        self.description = description
        self.completed = False
        self.due_date = None
        self.tags = []

    def set_due_date(self, due_date):
        self.due_date = due_date

    def set_tags(self, tags):
        self.tags = tags

    def mark_completed(self):
        self.completed = True

    def mark_pending(self):
        self.completed = False

    def display(self):
        status = "Completed" if self.completed else "Pending"
        due_date_str = f", Due: {self.due_date}" if self.due_date else ""
        tags_str = f", Tags: {', '.join(self.tags)}" if self.tags else ""
        return f"{self.description} - {status}{due_date_str}{tags_str}"


# TaskList class
  #it used to managing a list of tasks.    
class TaskList:
    def __init__(self):
        self.tasks = []
        self.undo_stack = []
        self.redo_stack = []

    def add_task(self, task):
        self.tasks.append(task)
        self.save_state()

    def delete_task(self, task):
        self.tasks.remove(task)
        self.save_state()

    def mark_completed(self, task):
        task.mark_completed()
        self.save_state()

    def mark_pending(self, task):
        task.mark_pending()
        self.save_state()

    def view_tasks(self, filter_type="all"):
        if filter_type == "completed":
            return [task.display() for task in self.tasks if task.completed]
        elif filter_type == "pending":
            return [task.display() for task in self.tasks if not task.completed]
        else:
            return [task.display() for task in self.tasks]

    def undo(self):
        if len(self.undo_stack) > 0:
            state = self.undo_stack.pop()
            self.redo_stack.append(Memento(self.tasks.copy()))
            self.tasks = state.get_state()

    def redo(self):
        if len(self.redo_stack) > 0:
            state = self.redo_stack.pop()
            self.undo_stack.append(Memento(self.tasks.copy()))
            self.tasks = state.get_state()

    def save_state(self):
        self.undo_stack.append(Memento(self.tasks.copy()))
        self.redo_stack = []


# Main Program
 # by using switch case system!        
task_list = TaskList()

while True:
    print("\n===== To-Do List Manager =====")
    print("1. Add Task")
    print("2. Mark Completed")
    print("3. Delete Task")
    print("4. View Tasks")
    print("5. Undo")
    print("6. Redo")
    print("0. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        description = input("Enter task description: ")
        due_date = input("Enter due date (optional, format: YYYY-MM-DD): ")
        tags = input("Enter tags (optional, separated by commas): ").split(', ')
        task_builder = TaskBuilder(description)
        if due_date:
            task_builder.set_due_date(due_date)
        if tags:
            task_builder.set_tags(tags)
        new_task = task_builder.build()
        task_list.add_task(new_task)
        print("Task added successfully!")

    elif choice == "2":
        task_description = input("Enter task description to mark as completed: ")
        task_to_mark = next((task for task in task_list.tasks if task.description == task_description), None)
        if task_to_mark:
            task_list.mark_completed(task_to_mark)
            print(f"Task '{task_description}' marked as completed.")
        else:
            print(f"Task '{task_description}' not found.")

    elif choice == "3":
        task_description = input("Enter task description to delete: ")
        task_to_delete = next((task for task in task_list.tasks if task.description == task_description), None)
        if task_to_delete:
            task_list.delete_task(task_to_delete)
            print(f"Task '{task_description}' deleted.")
        else:
            print(f"Task '{task_description}' not found.")

    elif choice == "4":
        filter_type = input("Enter filter type (all/completed/pending): ")
        tasks = task_list.view_tasks(filter_type)
        print("\n===== Tasks =====")
        for task in tasks:
            print(task)

    elif choice == "5":
        task_list.undo()
        print("Undo successful.")

    elif choice == "6":
        task_list.redo()
        print("Redo successful.")

    elif choice == "0":
        print("Exiting To-Do List Manager. Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")
