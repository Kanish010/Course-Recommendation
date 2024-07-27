import bcrypt
from mysql.connector import Error
from database import create_connection, close_connection

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
            # Check if username or email already exists
            cursor.execute("SELECT user_id FROM Users WHERE username = %s OR email = %s", (username, email))
            if cursor.fetchone():
                print("Error: Username or email already exists.")
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
            if record and verify_password(password, record[1]):
                print("User authenticated successfully")
                return record[0]  # Return the user_id
            else:
                print("Error: Invalid username or password.")
                return None
        except Error as e:
            print(f"Database Error: {e}")
            return None
        finally:
            cursor.close()
            close_connection(connection)