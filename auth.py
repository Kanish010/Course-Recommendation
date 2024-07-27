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
            cursor.execute(
                "INSERT INTO Users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            connection.commit()
            print("User registered successfully")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            close_connection(connection)

def authenticate_user(username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT password_hash FROM Users WHERE username = %s", (username,))
            record = cursor.fetchone()
            if record and verify_password(password, record[0]):
                print("User authenticated successfully")
                return True
            else:
                print("Authentication failed")
                return False
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            close_connection(connection)