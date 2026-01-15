import json
import os
import sys
from getpass import getpass
from pathlib import Path
from datetime import datetime

from models import TodoItem, Priority, Status

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
USERS_FILE = DATA_DIR / "users.json"
TODOS_FILE = DATA_DIR / "todos.json"


def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_users() -> list:
    if not USERS_FILE.exists():
        return []
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_users(users: list) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def find_user(users: list, username: str) -> dict | None:
    for u in users:
        if u.get("username") == username:
            return u
    return None


class TodoManager:
    def __init__(self):
        self.todos = self.load_todos()

    def load_todos(self) -> list:
        if not TODOS_FILE.exists():
            return []
        try:
            with open(TODOS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def save_todos(self) -> None:
        with open(TODOS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.todos, f, indent=2)

    def create_todo(self, title: str, details: str, priority: str, owner: str) -> TodoItem:
        """Create a new todo item."""
        priority_obj = Priority[priority.upper()] if priority.upper() in Priority.__members__ else Priority.MID
        todo = TodoItem(
            title=title,
            details=details,
            priority=priority_obj,
            owner=owner
        )
        self.todos.append(todo.to_dict())
        self.save_todos()
        return todo

    def get_todos_by_owner(self, owner: str) -> list:
        """Get all todos for a specific owner."""
        return [TodoItem.from_dict(t) for t in self.todos if t.get("owner") == owner]

    def get_todo_by_id(self, todo_id: str) -> TodoItem | None:
        """Get a specific todo by ID."""
        for t in self.todos:
            if t.get("id") == todo_id:
                return TodoItem.from_dict(t)
        return None

    def update_todo(self, todo_id: str, **kwargs) -> bool:
        """Update a todo item. Accepted kwargs: title, details, priority, status."""
        for i, t in enumerate(self.todos):
            if t.get("id") == todo_id:
                if "title" in kwargs:
                    t["title"] = kwargs["title"]
                if "details" in kwargs:
                    t["details"] = kwargs["details"]
                if "priority" in kwargs:
                    priority_obj = Priority[kwargs["priority"].upper()] if kwargs["priority"].upper() in Priority.__members__ else Priority.MID
                    t["priority"] = priority_obj.value
                if "status" in kwargs:
                    status_obj = Status[kwargs["status"].upper()] if kwargs["status"].upper() in Status.__members__ else Status.PENDING
                    t["status"] = status_obj.value
                t["updated_at"] = datetime.utcnow().isoformat()
                self.save_todos()
                return True
        return False

    def delete_todo(self, todo_id: str) -> bool:
        """Delete a todo item by ID."""
        for i, t in enumerate(self.todos):
            if t.get("id") == todo_id:
                self.todos.pop(i)
                self.save_todos()
                return True
        return False


def signup() -> None:
    print("== Sign Up ==")
    username = input("Username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return
    users = load_users()
    if find_user(users, username):
        print("User already exists.")
        return
    password = getpass("Password: ")
    users.append({"username": username, "password": password})
    save_users(users)
    print("Sign up successful. You can now log in.")


def login() -> str | None:
    print("== Login ==")
    username = input("Username: ").strip()
    password = getpass("Password: ")
    users = load_users()
    user = find_user(users, username)
    if not user or user.get("password") != password:
        print("Invalid credentials.")
        return None
    print(f"Welcome, {username}!")
    return username


def post_login_menu(username: str) -> None:
    """Main menu for logged-in users."""
    todo_manager = TodoManager()
    
    while True:
        print(f"\n=== Main Menu ({username}) ===")
        print("1) Create a to-do")
        print("2) View all to-dos")
        print("3) View to-do details")
        print("4) Mark to-do as completed")
        print("5) Edit a to-do")
        print("6) Delete a to-do")
        print("7) Logout")
        print()
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            create_todo_interactive(todo_manager, username)
        elif choice == "2":
            view_all_todos(todo_manager, username)
        elif choice == "3":
            view_todo_details(todo_manager, username)
        elif choice == "4":
            mark_todo_completed(todo_manager, username)
        elif choice == "5":
            edit_todo_interactive(todo_manager, username)
        elif choice == "6":
            delete_todo_interactive(todo_manager, username)
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Enter 1-7.")


def create_todo_interactive(todo_manager: TodoManager, username: str) -> None:
    """Interactive function to create a new todo."""
    print("\n=== Create a New To-Do ===")
    title = input("Title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    
    details = input("Details: ").strip()
    
    print("Priority: [HIGH / MID / LOW] (default: MID)")
    priority = input("Priority: ").strip().upper()
    if priority not in ["HIGH", "MID", "LOW"]:
        priority = "MID"
    
    todo = todo_manager.create_todo(title, details, priority, username)
    print(f"To-do created successfully! (ID: {todo.id})")


def view_all_todos(todo_manager: TodoManager, username: str) -> None:
    """View all todos for the logged-in user."""
    todos = todo_manager.get_todos_by_owner(username)
    
    if not todos:
        print("\nNo to-dos found.")
        return
    
    print(f"\n=== Your To-Dos ===")
    for todo in todos:
        status_marker = "✓" if todo.status == Status.COMPLETED else "○"
        print(f"{status_marker} [{todo.id[:8]}...] {todo.title} ({todo.priority.value})")


def view_todo_details(todo_manager: TodoManager, username: str) -> None:
    """View detailed information about a specific todo."""
    todos = todo_manager.get_todos_by_owner(username)
    
    if not todos:
        print("\nNo to-dos found.")
        return
    
    print("\n=== Select a To-Do to View ===")
    for i, todo in enumerate(todos, 1):
        status_marker = "✓" if todo.status == Status.COMPLETED else "○"
        print(f"{i}) {status_marker} {todo.title}")
    
    try:
        choice = int(input("Select a to-do (number): ").strip())
        if 1 <= choice <= len(todos):
            todo = todos[choice - 1]
            print("\n=== To-Do Details ===")
            print(f"ID: {todo.id}")
            print(f"Title: {todo.title}")
            print(f"Details: {todo.details if todo.details else '(no details)'}")
            print(f"Priority: {todo.priority.value}")
            print(f"Status: {todo.status.value}")
            print(f"Owner: {todo.owner}")
            print(f"Created: {todo.created_at}")
            print(f"Updated: {todo.updated_at}")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")


def mark_todo_completed(todo_manager: TodoManager, username: str) -> None:
    """Mark a todo as completed."""
    todos = todo_manager.get_todos_by_owner(username)
    
    if not todos:
        print("\nNo to-dos found.")
        return
    
    print("\n=== Mark To-Do as Completed ===")
    for i, todo in enumerate(todos, 1):
        status_marker = "✓" if todo.status == Status.COMPLETED else "○"
        print(f"{i}) {status_marker} {todo.title}")
    
    try:
        choice = int(input("Select a to-do (number): ").strip())
        if 1 <= choice <= len(todos):
            todo = todos[choice - 1]
            if todo.status == Status.COMPLETED:
                print(f"To-do '{todo.title}' is already completed.")
            else:
                todo_manager.update_todo(todo.id, status="COMPLETED")
                print(f"To-do '{todo.title}' marked as completed.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")


def edit_todo_interactive(todo_manager: TodoManager, username: str) -> None:
    """Edit an existing todo."""
    todos = todo_manager.get_todos_by_owner(username)
    
    if not todos:
        print("\nNo to-dos found.")
        return
    
    print("\n=== Edit a To-Do ===")
    for i, todo in enumerate(todos, 1):
        print(f"{i}) {todo.title}")
    
    try:
        choice = int(input("Select a to-do (number): ").strip())
        if 1 <= choice <= len(todos):
            todo = todos[choice - 1]
            print(f"\nEditing: {todo.title}")
            
            title = input("New title (leave empty to skip): ").strip()
            details = input("New details (leave empty to skip): ").strip()
            priority = input("New priority [HIGH/MID/LOW] (leave empty to skip): ").strip().upper()
            
            updates = {}
            if title:
                updates["title"] = title
            if details:
                updates["details"] = details
            if priority and priority in ["HIGH", "MID", "LOW"]:
                updates["priority"] = priority
            
            if updates:
                todo_manager.update_todo(todo.id, **updates)
                print("To-do updated successfully.")
            else:
                print("No changes made.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")


def delete_todo_interactive(todo_manager: TodoManager, username: str) -> None:
    """Delete a todo."""
    todos = todo_manager.get_todos_by_owner(username)
    
    if not todos:
        print("\nNo to-dos found.")
        return
    
    print("\n=== Delete a To-Do ===")
    for i, todo in enumerate(todos, 1):
        print(f"{i}) {todo.title}")
    
    try:
        choice = int(input("Select a to-do (number): ").strip())
        if 1 <= choice <= len(todos):
            todo = todos[choice - 1]
            confirm = input(f"Are you sure you want to delete '{todo.title}'? (yes/no): ").strip().lower()
            if confirm == "yes":
                todo_manager.delete_todo(todo.id)
                print("To-do deleted successfully.")
            else:
                print("Deletion cancelled.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")


def pre_login_menu() -> None:
    ensure_data_dir()
    while True:
        print("\nPre-Login Menu:\n1) Login\n2) Sign Up\n3) Exit\n")
        choice = input("Select an option: ").strip()
        if choice == "1":
            username = login()
            if username:
                post_login_menu(username)
        elif choice == "2":
            signup()
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")


if __name__ == "__main__":
    try:
        pre_login_menu()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(0)
