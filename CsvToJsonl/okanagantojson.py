import pandas as pd
import json

# List of interest terms for Okanagan campus from the course full names
okanagan_interest_terms = [
    "Anthropology", "Applied Science", "Art History and Visual Culture", 
    "Astronomy", "Biochemistry", "Biology", "Chemistry", 
    "Chinese", "Communications And Rhetoric", "Computer Engineering", 
    "Computer Science", "Cooperative Education", "Creative and Critical Studies", 
    "Creative Writing", "Cultural Studies", "Curriculum Studies", 
    "Data Science", "Design, Innovation, Creativity, Entrepreneurship", 
    "Digital Humanities", "Early Childhood Education", "Earth & Environmental Sciences", 
    "Economics", "Education", "Education Doctorate Leadership and Learning", 
    "Educational Administration", "Educational Psychology and Special Education", 
    "Educational Studies", "Educational Technology", "Engineering", 
    "English", "English for Academic Purposes", "Exchange Programs", 
    "Film", "Food Systems", "French", "Freshwater Science", 
    "Gender and Women's Studies", "Geography", "Geospatial Information Science", 
    "German", "Health & Exercise Sciences", "Health Studies", 
    "Health-Interprofessional", "Hebrew", "History", 
    "Immersive Technologies", "Indigenous Language", "Indigenous Studies", 
    "Interdisciplinary Graduate Studies", "Japanese Studies", "Korean", 
    "Language and Literacy Education", "Latin", "Management", 
    "Management Co-Op", "Manufacturing Engineering", "Mathematics", 
    "Media Studies", "Music", "Nle?kepmx Language", "Nsyilxcn", 
    "Nursing", "Philosophy", "Physics", "Political Science", 
    "Psychology", "Social and Economic Change", "Social Work", 
    "Sociology", "Spanish", "St'�t'imc Language", "Statistics", 
    "Sustainability", "Theatre", "Vantage College", "Visual Arts", 
    "World Literature"
]

def create_fine_tuning_data(courses_df, interest_terms):
    data = []
    for interest in interest_terms:
        for _, row in courses_df.iterrows():
            course_description = row['Course Description']
            if pd.isna(course_description):
                continue
            if interest.lower() in course_description.lower():
                prompt = f"Tell me about {interest} courses."
                completion = f"Course ID: {row['Course ID']}, Course Title: {row['Course Title']}, Course Description: {course_description}, Credits: {row['Credits']}"
                data.append({"prompt": prompt, "completion": completion})
    return data

def save_jsonl(data, output_jsonl):
    with open(output_jsonl, 'w') as outfile:
        for item in data:
            outfile.write(json.dumps(item) + '\n')

# Load Okanagan courses data
okanagan_courses = pd.read_csv('CourseData/ubc_okanagan_courses.csv')

# Create fine-tuning data for Okanagan
okanagan_fine_tuning_data = create_fine_tuning_data(okanagan_courses, okanagan_interest_terms)

# Save as JSONL
save_jsonl(okanagan_fine_tuning_data, 'CsvToJsonl/ubc_okanagan_courses.jsonl')

print("Okanagan fine-tuning data creation completed!")