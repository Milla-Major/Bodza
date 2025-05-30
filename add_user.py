import sqlite3
from getpass import getpass
from werkzeug.security import generate_password_hash

DB_PATH = "data/magazine_subscription.db"

def main():
    username = input("Username: ").strip()
    password = getpass("Password: ").strip()
    confirm = getpass("Password again: ").strip()

    if password != confirm:
        print("Both passwords must match!")
        return
    hash_pw = generate_password_hash(password)
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_pw))
            print(f"User '{username}' successfully added!")
    except sqlite3.IntegrityError:
        print("User already exists. Please choose a different username.")

if __name__ == "__main__":
    main()