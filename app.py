from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)

# Load and preprocess data
courses = pd.read_excel('courses.xlsx')
courses['Description'] = courses['Description'].fillna('')
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(courses['Description'])

@app.route('/recommend', methods=['GET'])
def recommend():
    field_of_interest = request.args.get('field_of_interest')
    interest_vector = tfidf.transform([field_of_interest])
    sim_scores = linear_kernel(interest_vector, tfidf_matrix).flatten()
    similar_indices = sim_scores.argsort()[-10:][::-1]
    similar_courses = courses.iloc[similar_indices]
    relevant_courses = similar_courses[similar_courses.apply(
        lambda row: field_of_interest.lower() in row['title'].lower() or field_of_interest.lower() in row['Description'].lower(), axis=1)]
    
    return jsonify(relevant_courses[['Title', 'Description']].to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
