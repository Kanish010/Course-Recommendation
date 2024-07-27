import mysql.connector
from mysql.connector import Error
import os

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='CourseRecommendationDB',
            user=os.getenv('DB_USER', 'username'),
            password=os.getenv('DB_PASSWORD', 'password')
        )
        return connection
    except Error as e:
        print(f"Database Connection Error: {e}")
        return None

def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()