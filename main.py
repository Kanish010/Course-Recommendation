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
    interest_filtered = data[
        data['Course Description'].str.contains(interest, case=False, na=False) |
        data['Course Title'].str.contains(interest, case=False, na=False)
    ]
    
    if levels:
        level_filtered = interest_filtered[interest_filtered['Level'].isin(levels)]
    else:
        level_filtered = interest_filtered
    
    level_filtered['Numeric Level'] = level_filtered['Level'].apply(lambda x: int(x) if x.isdigit() else 999)
    level_filtered = level_filtered.sort_values(by='Numeric Level')
    
    return level_filtered

# Main function to interact with the user
def main():
    valid_levels = {'100', '200', '300', '400', '500', '600', '700'}
    
    while True:
        campus = input("Which campus are you interested in? (Okanagan/Vancouver): ").strip().lower().replace(" ", "")
        if campus == 'okanagan':
            course_data = okanagan_courses
            break
        elif campus == 'vancouver':
            course_data = vancouver_courses
            break
        else:
            print("Invalid campus selection. Please enter 'Okanagan' or 'Vancouver'.")
    
    while True:
        user_interest = input("Please describe your area of interest: ").strip()
        if user_interest:
            break
        else:
            print("You did not provide an area of interest. Please try again.")
    
    while True:
        user_levels_input = input("Which course levels are you interested in? (100, 200, ..., 700, leave blank for all levels): ").strip().replace(" ", "")
        if user_levels_input:
            levels = user_levels_input.split(',')
            if all(level in valid_levels for level in levels):
                break
            else:
                print("Please enter valid course levels (100, 200, ..., 700) or leave blank for all levels.")
        else:
            levels = list(valid_levels)
            break
    
    recommended_courses = filter_courses(course_data, user_interest, levels)
    
    if not recommended_courses.empty:
        print("\nRecommended courses for you:")
        print(recommended_courses[['Course Title', 'Course ID', 'Course Description', 'Credits']].to_string(index=False))
    else:
        if levels and user_interest:
            print(f"\nNo {', '.join(levels)} level courses related to '{user_interest}' were found.")
        elif levels:
            print(f"\nNo courses found at {', '.join(levels)} level.")
        elif user_interest:
            print(f"\nNo courses found related to '{user_interest}'.")
        else:
            print("\nNo courses found matching your criteria.")
        
# Run the main function
if __name__ == "__main__":
    main()