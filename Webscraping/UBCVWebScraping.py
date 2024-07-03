import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of course IDs and their full names
course_id_mapping = {
    "adhe_v": "Adult and Higher Education", "afst_v": "African Studies", "agec_v": "Agricultural Economics",
    "asl_v": "American Sign Language", "anat_v": "Anatomy", "amne_v": "Ancient Mediterranean and Near Eastern Studies",
    "arcl_v": "Anthropological Archaeology", "anth_v": "Anthropology", "aanb_v": "Applied Animal Biology",
    "apbi_v": "Applied Biology", "apsc_v": "Applied Science", "appp_v": "Applied Science Professional Program Platform",
    "aqua_v": "Aquaculture", "arch_v": "Architecture", "arst_v": "Archival Studies", "arth_v": "Art History",
    "asic_v": "Arts and Science Interdisciplinary Courses", "artc_v": "Arts Co-Op", "arts_v": "Arts One Program",
    "astu_v": "Arts Studies", "acam_v": "Asian Canadian and Asian Migration Studies", "asla_v": "Asian Languages",
    "asia_v": "Asian Studies", "asix_v": "Asian Studies Crossings", "astr_v": "Astronomy", "atsc_v": "Atmospheric Science",
    "audi_v": "Audiology and Speech Sciences", "bioc_v": "Biochemistry", "fsct_v": "Biochemistry and Forensic Science",
    "biof_v": "Bioinformatics", "biol_v": "Biology", "bmeg_v": "Biomedical Engineering", "biot_v": "Biotechnology",
    "bota_v": "Botany", "brdg_v": "Bridge Program", "busi_v": "Business", "baac_v": "Business Administration: Accounting",
    "babs_v": "Business Administration: Business Statistics", "bait_v": "Business Administration: Business Technology Management",
    "ba_v": "Business Administration: Core", "baen_v": "Business Administration: Entrepreneurship",
    "bafi_v": "Business Administration: Finance", "bahr_v": "Business Administration: Human Resources Management",
    "bala_v": "Business Administration: Law", "bams_v": "Business Administration: Management Science",
    "bama_v": "Business Administration: Marketing", "bapa_v": "Business Administration: Policy Analysis",
    "basm_v": "Business Administration: Strategic Management", "basc_v": "Business Administration: Supply Chain",
    "baul_v": "Business Administration: Urban Land Economics", "cdst_v": "Canadian Studies", "cnto_v": "Cantonese",
    "ctln_v": "Catalan", "cell_v": "Cell and Developmental Biology", "phyl_v": "Cellular and Physiological Sciences",
    "caps_v": "Cellular, Anatomical and Physiological Sciences", "cens_v": "Central, Eastern and Northern European Studies",
    "ccfi_v": "Centre for Cross-Faculty Inquiry", "chbe_v": "Chemical and Biological Engineering", "chem_v": "Chemistry",
    "chil_v": "Children's Literature", "chin_v": "Chinese", "cmst_v": "Cinema and Media Studies", "cine_v": "Cinema Studies",
    "civl_v": "Civil Engineering", "arbc_v": "Classical Arabic", "clst_v": "Classical Studies", "ceen_v": "Clean Energy Engineering",
    "cogs_v": "Cognitive Systems Program", "comm_v": "Commerce", "coec_v": "Commerce Economics", "cohr_v": "Commerce Human Resources",
    "comr_v": "Commerce Minor", "plan_v": "Community and Regional Planning", "colx_v": "Computational Linguistics",
    "cpen_v": "Computer Engineering", "cpsc_v": "Computer Science", "cap_v": "Coordinated Arts Program",
    "cspw_v": "Coordinated Science Program Workshop", "cnps_v": "Counselling Psychology", "crwr_v": "Creative Writing",
    "ccst_v": "Critical and Curatorial Studies", "csis_v": "Critical Studies in Sexuality", "edcp_v": "Curriculum and Pedagogy",
    "dani_v": "Danish", "dsci_v": "Data Science", "dhyg_v": "Dental Hygiene", "dent_v": "Dentistry", "des_v": "Design",
    "dmed_v": "Digital Media", "medd_v": "Doctor of Medicine", "eced_v": "Early Childhood Education",
    "eosc_v": "Earth and Ocean Sciences", "econ_v": "Economics", "educ_v": "Education", "ecps_v": "Educational & Counselling Psychology, & Special Education",
    "epse_v": "Educational Psychology and Special Education", "edst_v": "Educational Studies", "etec_v": "Educational Technology",
    "eece_v": "Electrical and Computer Engineering", "elec_v": "Electrical Engineering", "enpp_v": "Engineering and Public Policy",
    "enph_v": "Engineering Physics", "engl_v": "English", "enst_v": "Environment and Sustainability",
    "enve_v": "Environmental Engineering", "envr_v": "Environmental Science", "iest_v": "European Studies", "exch_v": "Exchange Programs",
    "emba_v": "Executive M.B.A.", "fmpr_v": "Family Practice", "fmst_v": "Family Studies", "fipr_v": "Film Production",
    "fnel_v": "First Nations and Endangered Languages Program", "fnis_v": "First Nations and Indigenous Studies",
    "fish_v": "Fisheries Research", "fre_v": "Food and Resource Economics", "food_v": "Food Science",
    "fnh_v": "Food, Nutrition and Health", "best_v": "Forest Bioeconomy Sciences and Technology", "fopr_v": "Forest Operations",
    "frst_v": "Forestry", "fcor_v": "Forestry Core", "fope_v": "Forestry Online Professional Education",
    "fren_v": "French", "grsj_v": "Gender, Race, Sexuality and Social Justice", "gsat_v": "Genome Science and Technology",
    "geos_v": "Geographical Sciences", "geog_v": "Geography", "gem_v": "Geomatics for Environmental Management",
    "gern_v": "German", "gmst_v": "Germanic Studies", "grs_v": "Global Resource Systems", "grek_v": "Greek",
    "hgse_v": "Haida Gwaii Semesters", "heso_v": "Health and Society", "hebr_v": "Hebrew", "hpb_v": "High Performance Buildings",
    "hinu_v": "Hindi-Urdu", "hist_v": "History", "hunu_v": "Human Nutrition", "ils_v": "Indigenous Land Stewardship",
    "inlb_v": "Indigenous Land-Based Studies", "indo_v": "Indonesian", "info_v": "Information Studies", "iar_v": "Institute of Asian Research",
    "igen_v": "Integrated Engineering", "isci_v": "Integrated Sciences", "iwme_v": "Integrated Water Management Engineering",
    "rads_v": "Interdisciplinary Radiology", "inds_v": "Interdisciplinary Studies", "ital_v": "Italian", "japn_v": "Japanese",
    "jrnl_v": "Journalism", "kin_v": "Kinesiology", "korn_v": "Korean", "lfs_v": "Land & Food Systems", "lws_v": "Land and Water Systems",
    "larc_v": "Landscape Architecture", "lled_v": "Language and Literacy Education", "latn_v": "Latin",
    "last_v": "Latin American Studies", "law_v": "Law", "laso_v": "Law and Society", "libr_v": "Library and Information Studies",
    "lais_v": "Library, Archival and Information Studies", "ling_v": "Linguistics", "mgmt_v": "Management", "manu_v": "Manufacturing Engineering", "mrne_v": "Marine Science",
    "mtrl_v": "Materials Engineering", "math_v": "Mathematics", "mech_v": "Mechanical Engineering",
    "mdia_v": "Media Studies", "medg_v": "Medical Genetics", "medi_v": "Medicine",
    "mdvl_v": "Medieval Studies", "micb_v": "Microbiology", "mes_v": "Middle East Studies",
    "midw_v": "Midwifery", "mine_v": "Mining Engineering", "arbm_v": "Modern Standard Arabic",
    "musc_v": "Music", "nres_v": "Natural Resources", "cons_v": "Natural Resources Conservation",
    "name_v": "Naval Architecture and Marine Engineering", "nest_v": "Near Eastern Studies",
    "nepl_v": "Nepali", "nrsc_v": "Neuroscience", "nsci_v": "Neuroscience Undergraduate",
    "neur_v": "Neurosurgery", "nord_v": "Nordic Studies", "nurs_v": "Nursing",
    "obst_v": "Obstetrics and Gynaecology", "osot_v": "Occupational Science and Occupational Therapy",
    "onco_v": "Oncology", "obms_v": "Oral Biological Medical Sciences", "ohs_v": "Oral Health Sciences",
    "ornt_v": "Orientation to Medical School", "orpa_v": "Orthopaedics", "path_v": "Pathology",
    "pers_v": "Persian", "phar_v": "Pharmaceutical Sciences", "pcth_v": "Pharmacology and Therapeutics",
    "phrm_v": "Pharmacy", "phil_v": "Philosophy", "phth_v": "Physical Therapy",
    "phys_v": "Physics", "plnt_v": "Plant Science", "pols_v": "Polish",
    "poli_v": "Political Science", "port_v": "Portuguese", "psyt_v": "Psychiatry",
    "psyc_v": "Psychology", "ppga_v": "Public Policy And Global Affairs", "punj_v": "Punjabi",
    "radi_v": "Radiology", "rhsc_v": "Rehabilitation Sciences", "rgla_v": "Religion, Literature and The Arts",
    "relg_v": "Religious Studies", "res_v": "Resources, Environment and Sustainability",
    "rmst_v": "Romance Studies", "russ_v": "Russian", "sans_v": "Sanskrit",
    "spha_v": "School of Population & Public Health", "spph_v": "School of Population & Public Health",
    "scie_v": "Science", "sts_v": "Science and Technology Studies", "slav_v": "Slavic Studies",
    "sges_v": "Smart Grid Energy Systems", "sowk_v": "Social Work", "soci_v": "Sociology",
    "soil_v": "Soil Science", "soal_v": "South Asian Languages", "seal_v": "Southeast Asian Languages",
    "span_v": "Spanish", "stat_v": "Statistics", "rgst_v": "Study of Religion",
    "surg_v": "Surgery", "spe_v": "Sustainable Process Engineering", "swah_v": "Swahili",
    "swed_v": "Swedish", "libe_v": "Teacher Librarianship", "thtr_v": "Theatre",
    "thfl_v": "Theatre And Film", "tibt_v": "Tibetan Languages", "ukrn_v": "Ukrainian",
    "writ_v": "University Writing Centre Courses", "udes_v": "Urban Design",
    "ufor_v": "Urban Forestry", "urst_v": "Urban Studies", "ursy_v": "Urban Systems",
    "urol_v": "Urological Surgery", "vant_v": "Vantage College", "visa_v": "Visual Arts",
    "vrhc_v": "Vocational Rehabilitation Counselling", "wach_v": "Women+ and Children's Health Sciences",
    "wood_v": "Wood Products Processing", "wrds_v": "Writing, Research, and Discourse Studies",
    "ydsh_v": "Yiddish", "zool_v": "Zoology"
}

# Base URL for subjects
base_url = "https://vancouver.calendar.ubc.ca/course-descriptions/subject/"

# Generate subject URLs
subject_urls = [base_url + course_id.replace("_", "").lower() for course_id in course_id_mapping.keys()]

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
            if len(parts) < 2:
                i += 1
                continue  # Skip lines that don't have the expected format
            course_info = parts[0].strip()
            credits = parts[1].split(')')[0].strip()
            
            # Further split course info to get ID and number
            course_info_parts = course_info.rsplit(' ', 1)
            course_id = course_info_parts[0] + " " + course_info_parts[1]

            # The next line should contain the course title
            i += 1
            if i < len(lines):
                course_title = lines[i].strip()
            else:
                course_title = ""

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
csv_file_path = 'ubc_vancouver_courses.csv'
df.to_csv(csv_file_path, index=False)

print(f"Data has been scraped and saved to {csv_file_path}")