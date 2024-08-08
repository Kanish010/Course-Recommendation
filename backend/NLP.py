from openai import OpenAI
import os
from database import create_connection, close_connection
from course_recommendation import recommend_courses

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_response_from_gpt3(prompt):
    response = client.completions.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def process_user_input(user_id, user_input):
    db = create_connection()
    cursor = db.cursor()
    
    # Initial search
    if "search" in user_input:
        campus = input("Which campus are you interested in? (Okanagan/Vancouver): ").strip().lower()
        user_interest = input("Please describe your area of interest: ").strip()
        user_levels_input = input("Which course levels are you interested in? (100, 200, ..., 700, leave blank for all levels): ").strip()
        levels = user_levels_input.split(',') if user_levels_input else ["All Levels"]
        recommended_courses = recommend_courses(cursor, campus, user_interest, levels)
        response = "\nRecommended courses for you:\n" + "\n".join([f"Course Code: {course[0]}, Course Title: {course[1]}" for course in recommended_courses])
    else:
        # Refine search
        response = get_response_from_gpt3(user_input)
    
    close_connection(db)
    return response