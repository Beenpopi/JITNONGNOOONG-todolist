import json
import os
import sys
from getpass import getpass
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
USERS_FILE = DATA_DIR / "users.json"


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


def login() -> bool:
    print("== Login ==")
    username = input("Username: ").strip()
    password = getpass("Password: ")
    users = load_users()
    user = find_user(users, username)
    if not user or user.get("password") != password:
        print("Invalid credentials.")
        return False
    print(f"Welcome, {username}!")
    return True


def pre_login_menu() -> None:
    ensure_data_dir()
    while True:
        print("\nPre-Login Menu:\n1) Login\n2) Sign Up\n3) Exit\n")
        choice = input("Select an option: ").strip()
        if choice == "1":
            if login():
                print("(Logged in) — further app functionality not implemented yet.")
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
