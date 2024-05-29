# File path: course_recommendation_system.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load course data from Excel
def load_course_data(filepath):
    return pd.read_excel(filepath)

# Preprocess the course data
def preprocess_courses(courses):
    courses['description'] = courses['description'].fillna('')
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(courses['description'])
    return tfidf, tfidf_matrix

# Build content-based filtering model
def build_content_based_model(tfidf_matrix):
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    return cosine_sim

# Get content-based recommendations
def get_content_based_recommendations(field_of_interest, courses, tfidf, tfidf_matrix):
    # Transform the field of interest using the same TF-IDF vectorizer
    interest_vector = tfidf.transform([field_of_interest])
    
    # Compute similarity scores between the interest vector and course descriptions
    sim_scores = linear_kernel(interest_vector, tfidf_matrix).flatten()
    
    # Get indices of the top 10 most similar courses
    similar_indices = sim_scores.argsort()[-10:][::-1]
    similar_courses = courses.iloc[similar_indices]
    
    # Filter courses based on relevance to the user's field of interest
    relevant_courses = similar_courses[similar_courses.apply(lambda row: field_of_interest.lower() in row['title'].lower() or field_of_interest.lower() in row['description'].lower(), axis=1)]
    
    return relevant_courses

def main():
    # Load data
    courses = load_course_data('courses.xlsx')
    
    # Preprocess data
    tfidf, tfidf_matrix = preprocess_courses(courses)
    
    while True:
        user_input = input("Enter your field of interest (or type 'exit' to quit): ").strip()
        if user_input.lower() == 'exit':
            break
        
        # Content-based recommendations
        content_recommendations = get_content_based_recommendations(user_input, courses, tfidf, tfidf_matrix)
        if not content_recommendations.empty:
            print("\nContent-Based Recommendations:")
            print(content_recommendations[['title', 'description']].to_string(index=False))
        else:
            print("No courses found for the given field of interest.")
        
        print("\n")

if __name__ == '__main__':
    main()
