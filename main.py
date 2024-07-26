import pandas as pd
import re

# Load the CSV files for both campuses
okanagan_file_path = 'CourseData/ubc_okanagan_courses.csv'
vancouver_file_path = 'CourseData/ubc_vancouver_courses.csv'

okanagan_courses = pd.read_csv(okanagan_file_path)
vancouver_courses = pd.read_csv(vancouver_file_path)

# Function to extract and categorize course level from the 'Course ID'
def extract_and_categorize_level(course_id):
    # Extract the last three digits as the course level
    match = re.search(r'(\d{3})$', course_id)
    if match:
        level = int(match.group(1))
        # Determine the broad category by integer division
        if 100 <= level < 500:
            return str((level // 100) * 100)
        else:
            return 'Other'
    return 'Unknown'

# Function to prepare the courses DataFrame
def prepare_courses(courses_df):
    courses_df['Level'] = courses_df['Course ID'].apply(extract_and_categorize_level)
    return courses_df

# Prepare both course DataFrames
okanagan_courses = prepare_courses(okanagan_courses)
vancouver_courses = prepare_courses(vancouver_courses)

# Function to filter courses based on interest and levels
def filter_courses(data, interest, levels):
    # Filter by interest
    interest_filtered = data[
        data['Course Description'].str.contains(interest, case=False, na=False) |
        data['Course Title'].str.contains(interest, case=False, na=False)
    ]
    
    # Filter by levels if specified
    if levels:
        level_filtered = interest_filtered[interest_filtered['Level'].isin(levels)]
    else:
        level_filtered = interest_filtered
    
    # Sort courses by numeric level value from lowest to highest
    level_filtered['Numeric Level'] = level_filtered['Level'].apply(lambda x: int(x) if x.isdigit() else 999)
    level_filtered = level_filtered.sort_values(by='Numeric Level')
    
    return level_filtered

# Main function to interact with the user
def main():
    # Step 1: Ask for campus preference in a loop until valid input is received
    while True:
        campus = input("Which campus are you interested in? (Okanagan/Vancouver): ").strip().lower()
        if campus == 'okanagan':
            course_data = okanagan_courses
            break
        elif campus == 'vancouver':
            course_data = vancouver_courses
            break
        else:
            print("Invalid campus selection. Please enter 'Okanagan' or 'Vancouver'.")
    
    # Step 2: Get user interests
    user_interest = input("Please describe your area of interest: ").strip()
    
    # Step 3: Get user course level preference
    user_levels = input("Which course levels are you interested in? (e.g., 100, 200, leave blank for all levels): ").strip()
    
    # Parse the levels input and convert to string, ensuring no extra spaces
    levels = [level.strip() for level in user_levels.split(',')] if user_levels else []
    
    # Filter courses based on user input
    recommended_courses = filter_courses(course_data, user_interest, levels)
    
    # Display the results without the 'Level' column and index
    if not recommended_courses.empty:
        print("\nRecommended courses for you:")
        print(recommended_courses[['Course Title', 'Course ID', 'Course Description', 'Credits']].to_string(index=False))
    else:
        print("\nNo courses found matching your criteria.")
        
# Run the main function
if __name__ == "__main__":
    main()