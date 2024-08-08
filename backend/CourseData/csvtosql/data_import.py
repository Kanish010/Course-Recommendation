import pandas as pd
import mysql.connector

# Load the CSV files
okanagan_courses = pd.read_csv('CourseData/ubc_okanagan_courses.csv')
vancouver_courses = pd.read_csv('CourseData/ubc_vancouver_courses.csv')

# Add a 'Campus' column
okanagan_courses['Campus'] = 'Okanagan'
vancouver_courses['Campus'] = 'Vancouver'

# Combine the courses into a single DataFrame
all_courses = pd.concat([okanagan_courses, vancouver_courses])

# Fill NaN values with default values
all_courses['Subject'].fillna('Unknown Subject', inplace=True)
all_courses['Course ID'].fillna('', inplace=True)
all_courses['Course Title'].fillna('No Title', inplace=True)
all_courses['Course Description'].fillna('No Description', inplace=True)
all_courses['Credits'].fillna('0', inplace=True)
all_courses['Campus'].fillna('Unknown', inplace=True)

# Establish database connection
db = mysql.connector.connect(
    host="localhost",
    user="username",
    password="password",
    database="CourseRecommendationDB"
)

cursor = db.cursor()

# Insert courses into the Courses table
for _, row in all_courses.iterrows():
    if row['Course ID'] and row['Course Title']:  # Ensure essential fields are not empty
        cursor.execute("""
            INSERT INTO Courses (Subject, `Course ID`, `Course Title`, `Course Description`, Credits, Campus)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            Subject = VALUES(Subject),
            `Course Title` = VALUES(`Course Title`),
            `Course Description` = VALUES(`Course Description`),
            Credits = VALUES(Credits),
            Campus = VALUES(Campus)
        """, (row['Subject'], row['Course ID'], row['Course Title'], row['Course Description'], row['Credits'], row['Campus']))
        db.commit()

cursor.close()
db.close()