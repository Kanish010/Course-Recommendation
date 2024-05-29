from flask import Flask, request, render_template
import pandas as pd
import nltk
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)

# Load course data from Excel
def load_course_data(filepath):
    return pd.read_excel(filepath)

# Preprocess the course data
def preprocess_courses(courses):
    courses['description'] = courses['description'].fillna('')
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(courses['description'])
    return tfidf, tfidf_matrix

# Expand the field of interest with synonyms
def expand_with_synonyms(field_of_interest):
    synonyms = set()
    for syn in wordnet.synsets(field_of_interest):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
    return list(synonyms)

# Get content-based recommendations
def get_content_based_recommendations(field_of_interest, courses, tfidf, tfidf_matrix):
    expanded_interests = expand_with_synonyms(field_of_interest)
    expanded_interests.append(field_of_interest)  # Include the original term
    interest_vector = tfidf.transform(expanded_interests)
    
    # Compute similarity scores between the interest vector and course descriptions
    sim_scores = linear_kernel(interest_vector, tfidf_matrix).flatten()
    
    # Get indices of the top similar courses, ensuring not to go out of bounds
    similar_indices = sim_scores.argsort()[-10:][::-1]
    similar_indices = [i for i in similar_indices if i < len(courses)]
    similar_courses = courses.iloc[similar_indices]
    
    # Filter courses based on relevance to the user's field of interest or synonyms
    relevant_courses = similar_courses[similar_courses.apply(
        lambda row: any(interest.lower() in row['title'].lower() or interest.lower() in row['description'].lower() for interest in expanded_interests), axis=1)]
    
    return relevant_courses

# Initialize the data and model
courses = load_course_data('courses.xlsx')
tfidf, tfidf_matrix = preprocess_courses(courses)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    field_of_interest = request.form.get('field_of_interest')
    if not field_of_interest:
        return render_template('index.html', error="Field of interest is required")
    
    content_recommendations = get_content_based_recommendations(field_of_interest, courses, tfidf, tfidf_matrix)
    
    if not content_recommendations.empty:
        return render_template('index.html', recommendations=content_recommendations[['title', 'description']].to_dict(orient='records'))
    else:
        return render_template('index.html', error="No courses found for the given field of interest")

if __name__ == '__main__':
    nltk.download('wordnet')  # Ensure WordNet data is downloaded
    app.run(debug=True)
