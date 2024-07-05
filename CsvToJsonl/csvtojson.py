import pandas as pd
import json

# List of interest terms from the course full names
interest_terms = [
    "Adult and Higher Education", "African Studies", "Agricultural Economics",
    "American Sign Language", "Anatomy", "Ancient Mediterranean and Near Eastern Studies",
    "Anthropological Archaeology", "Anthropology", "Applied Animal Biology",
    "Applied Biology", "Applied Science", "Applied Science Professional Program Platform","Aquaculture", "Architecture", "Archival Studies", "Art History",
    "Arts and Science Interdisciplinary Courses", "Arts Co-Op", "Arts One Program",
    "Arts Studies", "Asian Canadian and Asian Migration Studies", "Asian Languages",
    "Asian Studies", "Asian Studies Crossings", "Astronomy", "Atmospheric Science",
    "Audiology and Speech Sciences", "Biochemistry", "Biochemistry and Forensic Science","Bioinformatics", "Biology", "Biomedical Engineering", "Biotechnology",
    "Botany", "Bridge Program", "Business", "Business Administration: Accounting",
    "Business Administration: Business Statistics", "Business Administration: Business Technology Management",
    "Business Administration: Core", "Business Administration: Entrepreneurship",
    "Business Administration: Finance", "Business Administration: Human Resources Management",
    "Business Administration: Law", "Business Administration: Management Science",
    "Business Administration: Marketing", "Business Administration: Policy Analysis",
    "Business Administration: Strategic Management", "Business Administration: Supply Chain",
    "Business Administration: Urban Land Economics", "Canadian Studies", "Cantonese",
    "Catalan", "Cell and Developmental Biology", "Cellular and Physiological Sciences",
    "Cellular, Anatomical and Physiological Sciences", "Central, Eastern and Northern European Studies",
    "Centre for Cross-Faculty Inquiry", "Chemical and Biological Engineering", "Chemistry",
    "Children's Literature", "Chinese", "Cinema and Media Studies", "Cinema Studies",
    "Civil Engineering", "Classical Arabic", "Classical Studies", "Clean Energy Engineering",
    "Cognitive Systems Program", "Commerce", "Commerce Economics", "Commerce Human Resources",
    "Commerce Minor", "Community and Regional Planning", "Computational Linguistics",
    "Computer Engineering", "Computer Science", "Coordinated Arts Program",
    "Coordinated Science Program Workshop", "Counselling Psychology", "Creative Writing",
    "Critical and Curatorial Studies", "Critical Studies in Sexuality", "Curriculum and Pedagogy",
    "Danish", "Data Science", "Dental Hygiene", "Dentistry", "Design",
    "Digital Media", "Doctor of Medicine", "Early Childhood Education",
    "Earth and Ocean Sciences", "Economics", "Education", "Educational & Counselling Psychology, & Special Education",
    "Educational Psychology and Special Education", "Educational Studies", "Educational Technology",
    "Electrical and Computer Engineering", "Electrical Engineering", "Engineering and Public Policy",
    "Engineering Physics", "English", "Environment and Sustainability",
    "Environmental Engineering", "Environmental Science", "European Studies", "Exchange Programs",
    "Executive M.B.A.", "Family Practice", "Family Studies", "Film Production",
    "First Nations and Endangered Languages Program", "First Nations and Indigenous Studies",
    "Fisheries Research", "Food and Resource Economics", "Food Science",
    "Food, Nutrition and Health", "Forest Bioeconomy Sciences and Technology", "Forest Operations",
    "Forestry", "Forestry Core", "Forestry Online Professional Education",
    "French", "Gender, Race, Sexuality and Social Justice", "Genome Science and Technology",
    "Geographical Sciences", "Geography", "Geomatics for Environmental Management","German", "Germanic Studies", "Global Resource Systems", "Greek",
    "Haida Gwaii Semesters", "Health and Society", "Hebrew", "High Performance Buildings",
    "Hindi-Urdu", "History", "Human Nutrition", "Indigenous Land Stewardship",
    "Indigenous Land-Based Studies", "Indonesian", "Information Studies", "Institute of Asian Research",
    "Integrated Engineering", "Integrated Sciences", "Integrated Water Management Engineering",
    "Interdisciplinary Radiology", "Interdisciplinary Studies", "Italian", "Japanese",
    "Journalism", "Kinesiology", "Korean", "Land & Food Systems", "Land and Water Systems","Landscape Architecture", "Language and Literacy Education", "Latin",
    "Latin American Studies", "Law", "Law and Society", "Library and Information Studies",
    "Library, Archival and Information Studies", "Linguistics", "Management",
    "Manufacturing Engineering", "Marine Science", "Materials Engineering",
    "Mathematics", "Mechanical Engineering", "Media Studies", "Medical Genetics",
    "Medicine", "Medieval Studies", "Microbiology", "Middle East Studies",
    "Midwifery", "Mining Engineering", "Modern Standard Arabic", "Music",
    "Natural Resources", "Natural Resources Conservation", "Naval Architecture and Marine Engineering",
    "Near Eastern Studies", "Nepali", "Neuroscience", "Neuroscience Undergraduate","Neurosurgery", "Nordic Studies", "Nursing", "Obstetrics and Gynaecology",
    "Occupational Science and Occupational Therapy", "Oncology", "Oral Biological Medical Sciences",
    "Oral Health Sciences", "Orientation to Medical School", "Orthopaedics", "Pathology",
    "Persian", "Pharmaceutical Sciences", "Pharmacology and Therapeutics","Pharmacy", "Philosophy", "Physical Therapy", "Physics",
    "Plant Science", "Polish", "Political Science", "Portuguese", "Psychiatry",
    "Psychology", "Public Policy And Global Affairs", "Punjabi", "Radiology",
    "Rehabilitation Sciences", "Religion, Literature and The Arts", "Religious Studies",
    "Resources, Environment and Sustainability", "Romance Studies", "Russian", "Sanskrit",
    "School of Population & Public Health", "Science", "Science and Technology Studies",
    "Slavic Studies", "Smart Grid Energy Systems", "Social Work", "Sociology",
    "Soil Science", "South Asian Languages", "Southeast Asian Languages","Spanish", "Statistics", "Study of Religion", "Surgery",
    "Sustainable Process Engineering", "Swahili", "Swedish", "Teacher Librarianship","Theatre", "Theatre And Film", "Tibetan Languages", "Ukrainian",
    "University Writing Centre Courses", "Urban Design", "Urban Forestry",
    "Urban Studies", "Urban Systems", "Urological Surgery", "Vantage College",
    "Visual Arts", "Vocational Rehabilitation Counselling", "Women+ and Children's Health Sciences",
    "Wood Products Processing", "Writing, Research, and Discourse Studies",
    "Yiddish", "Zoology", "Anthropology", "Applied Science", "Art History and Visual Culture", "Astronomy", "Biochemistry", "Biology", "Chemistry", 
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
    "German", "Health & Exercise Sciences", "Health Studies", "Health-Interprofessional", "Hebrew", "History", 
    "Immersive Technologies", "Indigenous Language", "Indigenous Studies", 
    "Interdisciplinary Graduate Studies", "Japanese Studies", "Korean", "Language and Literacy Education", "Latin", "Management", 
    "Management Co-Op", "Manufacturing Engineering", "Mathematics", 
    "Media Studies", "Music", "Nle?kepmx Language", "Nsyilxcn", 
    "Nursing", "Philosophy", "Physics", "Political Science", 
    "Psychology", "Social and Economic Change", "Social Work", 
    "Sociology", "Spanish", "St'�t'imc Language", "Statistics", 
    "Sustainability", "Theatre", "Vantage College", "Visual Arts", "World Literature"
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

# Load courses data
vancouver_courses = pd.read_csv('CourseData/ubc_vancouver_courses.csv')
okanagan_courses = pd.read_csv('CourseData/ubc_okanagan_courses.csv')

# Create fine-tuning data
vancouver_fine_tuning_data = create_fine_tuning_data(vancouver_courses, interest_terms)
okanagan_fine_tuning_data = create_fine_tuning_data(okanagan_courses, interest_terms)

# Save as JSONL
save_jsonl(vancouver_fine_tuning_data, 'CsvToJsonl/ubc_vancouver_courses_fine_tuning.jsonl')
save_jsonl(okanagan_fine_tuning_data, 'CsvToJsonl/ubc_okanagan_courses_fine_tuning.jsonl')

print("Fine-tuning data creation completed!")