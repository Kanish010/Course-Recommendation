import pandas as pd
from _mysql_connector import Error
from database import create_connection, close_connection

def import_courses(file_path, campus):
    df = pd.read_csv(file_path)
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        for _, row in df.iterrows():
            try:
                cursor.execute(
                    "INSERT INTO Courses (course_title, course_description, course_level, course_credits, campus) VALUES (%s, %s, %s, %s, %s)",
                    (row['Course Title'], row['Course Description'], row['Level'], row['Credits'], campus)
                )
            except Error as e:
                print(f"Error: {e}")
        connection.commit()
        close_connection(connection)

if __name__ == "__main__":
    import_courses('CourseData/ubc_okanagan_courses.csv', 'Okanagan')
    import_courses('CourseData/ubc_vancouver_courses.csv', 'Vancouver')