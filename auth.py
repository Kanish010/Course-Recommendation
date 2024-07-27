import bcrypt
from mysql.connector import Error
from database import create_connection, close_connection
from datetime import datetime

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def register_user(username, email, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        hashed_password = hash_password(password)
        try:
            # Check if username already exists
            cursor.execute("SELECT user_id FROM Users WHERE username = %s", (username,))
            if cursor.fetchone():
                print("Error: Username already exists. Please choose a different username.")
                return None
            
            # Check if email already exists
            cursor.execute("SELECT user_id FROM Users WHERE email = %s", (email,))
            if cursor.fetchone():
                print("Error: Email already exists. Please choose a different email.")
                return None
            
            cursor.execute(
                "INSERT INTO Users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            user_id = cursor.lastrowid
            connection.commit()
            print("User registered successfully")
            return user_id
        except Error as e:
            print(f"Database Error: {e}")
            return None
        finally:
            cursor.close()
            close_connection(connection)

def authenticate_user(username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT user_id, password_hash FROM Users WHERE username = %s", (username,))
            record = cursor.fetchone()
            if not record:
                print("Error: Username does not exist. Please check your username.")
                return None
            elif not verify_password(password, record[1]):
                print("Error: Incorrect password. Please check your password.")
                return None
            else:
                # Update the last_login field to current timestamp
                cursor.execute(
                    "UPDATE Users SET last_login = %s WHERE user_id = %s",
                    (datetime.now(), record[0])
                )
                connection.commit()
                print("User authenticated successfully")
                return record[0]  # Return the user_id
        except Error as e:
            print(f"Database Error: {e}")
            return None
        finally:
            cursor.close()
            close_connection(connection)