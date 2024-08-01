from auth import register_user, authenticate_user
from database import create_connection, close_connection

def handle_registration():
    username = input("Enter a username: ").strip()
    email = input("Enter your email: ").strip()
    password = input("Enter a password: ").strip()
    
    user_id = register_user(username, email, password)
    if user_id is None:
        print("Registration failed. Please try again.")
    else:
        print(f"User {username} registered successfully")
    return user_id

def handle_login():
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    
    user_id = authenticate_user(username, password)
    if user_id is None:
        db = create_connection()
        cursor = db.cursor()
        cursor.execute("SELECT username FROM Users WHERE username = %s", (username,))
        if cursor.fetchone():
            print("Password is incorrect. Please try again.")
        else:
            print("Username does not exist. Please register.")
        close_connection(db)
    else:
        print(f"User {username} authenticated successfully")
    return user_id