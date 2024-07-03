
import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of URLs for each subject
subject_urls = [
    "https://vancouver.calendar.ubc.ca/course-descriptions/subject/adhev",
    # Add all other subject URLs here
]

# Lists to store the course data
course_ids = []
course_titles = []
course_descriptions = []
course_credits = []

# Function to check if a line of text contains the credits
def contains_credits(text):
    return "(3)" in text or "(4)" in text or "(6)" in text or "3-6" in text

# Loop through each subject URL
for url in subject_urls:
    # Send a GET request to the page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Get all text content
    page_text = soup.get_text(separator="\n", strip=True)
    
    # Split the text by lines
    lines = page_text.split("\n")
    
    # Iterate over the lines and capture course information
    i = 0
    while i < len(lines):
        line = lines[i]
        if contains_credits(line):
            # Extract the course ID and credits
            parts = line.split('(')
            course_info = parts[0].strip()
            credits = parts[1].split(')')[0].strip()
            
            # Further split course info to get ID and number
            course_info_parts = course_info.rsplit(' ', 1)
            course_id = course_info_parts[0] + " " + course_info_parts[1]

            # The next line should contain the course title
            i += 1
            course_title = lines[i].strip()
            
            # Move to the next line to collect course description
            i += 1
            description_lines = []
            while i < len(lines) and not contains_credits(lines[i]) and not lines[i].startswith(course_id.split()[0]):
                description_lines.append(lines[i])
                i += 1
            course_description = " ".join(description_lines).strip()
            
            # Append the data to lists
            course_ids.append(course_id)
            course_titles.append(course_title)
            course_credits.append(f"\t{credits}")
            course_descriptions.append(course_description)
        else:
            i += 1

# Create a DataFrame from the lists
df = pd.DataFrame({
    'Course ID': course_ids,
    'Course Title': course_titles,
    'Course Description': course_descriptions,
    'Credits': course_credits
}, dtype=str)

# Save the DataFrame to a CSV file in the current working directory
csv_file_path = 'ubc_okanagan_courses_filtered.csv'
df.to_csv(csv_file_path, index=False)

print(f"Data has been scraped and saved to {csv_file_path}")