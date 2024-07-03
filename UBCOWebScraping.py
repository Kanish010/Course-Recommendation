import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of course IDs and their full names
course_id_mapping = {
    "anth_o": "Anthropology", "apsc_o": "Applied Science", "arth_o": "Art History and Visual Culture", 
    "astr_o": "Astronomy", "bioc_o": "Biochemistry", "biol_o": "Biology", "chem_o": "Chemistry", 
    "chin_o": "Chinese", "corh_o": "Communications And Rhetoric", "cmpe_o": "Computer Engineering", 
    "cosc_o": "Computer Science", "coop_o": "Cooperative Education", "ccs_o": "Creative and Critical Studies", 
    "crwr_o": "Creative Writing", "cult_o": "Cultural Studies", "cust_o": "Curriculum Studies", 
    "data_o": "Data Science", "dice_o": "Design, Innovation, Creativity, Entrepreneurship", 
    "dihu_o": "Digital Humanities", "eced_o": "Early Childhood Education", "eesc_o": "Earth & Environmental Sciences", 
    "econ_o": "Economics", "educ_o": "Education", "edll_o": "Education Doctorate Leadership and Learning", 
    "eadm_o": "Educational Administration", "epse_o": "Educational Psychology and Special Education", 
    "edst_o": "Educational Studies", "etec_o": "Educational Technology", "engr_o": "Engineering", 
    "engl_o": "English", "eap_o": "English for Academic Purposes", "exch_o": "Exchange Programs", 
    "film_o": "Film", "fdsy_o": "Food Systems", "fren_o": "French", "fwsc_o": "Freshwater Science", 
    "gwst_o": "Gender and Women's Studies", "geog_o": "Geography", "gisc_o": "Geospatial Information Science", 
    "germ_o": "German", "hes_o": "Health & Exercise Sciences", "heal_o": "Health Studies", 
    "hint_o": "Health-Interprofessional", "hebr_o": "Hebrew", "hist_o": "History", 
    "imtc_o": "Immersive Technologies", "inlg_o": "Indigenous Language", "indg_o": "Indigenous Studies", 
    "igs_o": "Interdisciplinary Graduate Studies", "jpst_o": "Japanese Studies", "korn_o": "Korean", 
    "lled_o": "Language and Literacy Education", "latn_o": "Latin", "mgmt_o": "Management", 
    "mgco_o": "Management Co-Op", "manf_o": "Manufacturing Engineering", "math_o": "Mathematics", 
    "mdst_o": "Media Studies", "musc_o": "Music", "nlek_o": "Nle?kepmx Language", "nsyl_o": "Nsyilxcn", 
    "nrsg_o": "Nursing", "phil_o": "Philosophy", "phys_o": "Physics", "poli_o": "Political Science", 
    "psyo_o": "Psychology", "sech_o": "Social and Economic Change", "socw_o": "Social Work", 
    "soci_o": "Sociology", "span_o": "Spanish", "stmc_o": "St'�t'imc Language", "stat_o": "Statistics", 
    "sust_o": "Sustainability", "thtr_o": "Theatre", "vant_o": "Vantage College", "visa_o": "Visual Arts", 
    "wrld_o": "World Literature"
}

# Base URL for subjects
base_url = "https://okanagan.calendar.ubc.ca/course-descriptions/subject/"

# Generate subject URLs
subject_urls = [base_url + course_id.replace("_", "") for course_id in course_id_mapping.keys()]

# Lists to store the course data
course_ids_list = []
course_titles = []
course_descriptions = []
course_credits = []
course_full_names = []

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
            course_ids_list.append(course_id.upper())  # Ensure course IDs are in uppercase
            course_titles.append(course_title)
            course_credits.append(f"\t{credits}")
            course_descriptions.append(course_description)
            
            # Determine the full name for the current course ID
            for key, value in course_id_mapping.items():
                if key.replace("_", "") in url:
                    course_full_names.append(value)
                    break
        else:
            i += 1

# Create a DataFrame from the lists
df = pd.DataFrame({
    'Subject': course_full_names,
    'Course ID': course_ids_list,
    'Course Title': course_titles,
    'Course Description': course_descriptions,
    'Credits': course_credits
}, dtype=str)

# Save the DataFrame to a CSV file in the current working directory
csv_file_path = 'ubc_okanagan_courses.csv'
df.to_csv(csv_file_path, index=False)

print(f"Data has been scraped and saved to {csv_file_path}")