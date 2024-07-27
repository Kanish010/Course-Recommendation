import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='CourseRecommendationDB',
            user='your_username',  # Replace with your MySQL username
            password='your_password'  # Replace with your MySQL password
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
        print("MySQL connection is closed")