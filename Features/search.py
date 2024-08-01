from course_recommendation import recommend_courses
from database import create_connection, close_connection

def new_search(user_id):
    campus = input("Which campus are you interested in? (Okanagan/Vancouver): ").strip().lower().replace(" ", "")
    if campus not in ['okanagan', 'vancouver']:
        print("Invalid campus selection. Please enter 'Okanagan' or 'Vancouver'.")
        return

    user_interest = input("Please describe your area of interest: ").strip()
    if not user_interest:
        print("You did not provide an area of interest.")
        return
    
    user_levels_input = input("Which course levels are you interested in? (100, 200, ..., 700, leave blank for all levels): ").strip().replace(" ", "")
    levels = user_levels_input.split(',') if user_levels_input else ["All Levels"]
    levels = [level.strip() for level in levels if level.strip() in {'100', '200', '300', '400', '500', '600', '700'} or level == "All Levels"]

    perform_search(user_id, campus, user_interest, levels)

def perform_search(user_id, campus, user_interest, levels):
    db = create_connection()
    if db is None:
        print("Failed to connect to the database. Please try again later.")
        return

    cursor = db.cursor()
    levels_str = ",".join(levels) if levels != ["All Levels"] else "All Levels"
    cursor.execute("""
        INSERT INTO UserLastSearch (user_id, preferred_levels, interests, preferred_campus)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE preferred_levels=%s, interests=%s, preferred_campus=%s
    """, (user_id, levels_str, user_interest, campus, levels_str, user_interest, campus))
    db.commit()
    recommended_courses = recommend_courses(cursor, campus, user_interest, levels)
    
    result_count = len(recommended_courses) if recommended_courses else 0
    if result_count > 0:
        print("\nRecommended courses for you:")
        for course in recommended_courses:
            print(f"Course Code: {course[0]}, Course Title: {course[1]}")
    else:
        print(f"\nNo {', '.join(levels)} level courses with interest '{user_interest}' were found.")

    cursor.execute("""
        INSERT INTO UserSearchHistory (user_id, search_query, result_count)
        VALUES (%s, %s, %s)
    """, (user_id, f"Interest: {user_interest}, Levels: {levels_str}", result_count))
    db.commit()

    for course in recommended_courses:
        cursor.execute("""
            INSERT INTO RecommendedCourses (user_id, course_title, course_id, campus)
            VALUES (%s, %s, %s, %s)
        """, (user_id, course[1], course[0], campus))
    db.commit()

    close_connection(db)