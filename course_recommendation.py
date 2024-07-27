import pandas as pd
import re

# Load the CSV files for both campuses
okanagan_file_path = 'CourseData/ubc_okanagan_courses.csv'
vancouver_file_path = 'CourseData/ubc_vancouver_courses.csv'

okanagan_courses = pd.read_csv(okanagan_file_path)
vancouver_courses = pd.read_csv(vancouver_file_path)

# Function to extract and categorize course level from the 'Course ID'
def extract_and_categorize_level(course_id):
    match = re.search(r'(\d{3})$', course_id)
    if match:
        level = int(match.group(1))
        if 100 <= level <= 799:
            return str((level // 100) * 100)
    return 'Other'

# Prepare the courses DataFrame by extracting course levels
def prepare_courses(courses_df):
    courses_df['Level'] = courses_df['Course ID'].apply(extract_and_categorize_level)
    return courses_df

okanagan_courses = prepare_courses(okanagan_courses)
vancouver_courses = prepare_courses(vancouver_courses)

# Filter courses based on interest and levels
def filter_courses(data, interest, levels):
    interest_filtered = data[
        data['Course Description'].str.contains(interest, case=False, na=False) |
        data['Course Title'].str.contains(interest, case=False, na=False)
    ]
    
    if levels:
        interest_filtered = interest_filtered[interest_filtered['Level'].isin(levels)]
    
    return interest_filtered.sort_values(by='Level')

# Function to recommend courses based on user input
def recommend_courses(campus, interest, levels):
    if campus == 'okanagan':
        course_data = okanagan_courses
    elif campus == 'vancouver':
        course_data = vancouver_courses
    else:
        raise ValueError("Invalid campus selection.")
    
    recommended_courses = filter_courses(course_data, interest, levels)
    return recommended_courses[['Course Title', 'Course ID']]