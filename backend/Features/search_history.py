from database import create_connection, close_connection

def get_search_history(user_id):
    db = create_connection()
    if db is None:
        return {"error": "Failed to connect to the database."}

    cursor = db.cursor()
    cursor.execute("""
        SELECT search_id, search_query, result_count, search_date
        FROM UserSearchHistory
        WHERE user_id = %s
        ORDER BY search_date DESC
    """, (user_id,))
    searches = cursor.fetchall()

    history = []
    for search in searches:
        cursor.execute("""
            SELECT course_title, course_id, campus
            FROM RecommendedCourses
            WHERE user_id = %s AND search_id = %s
        """, (user_id, search[0]))
        recommended_courses = cursor.fetchall()

        history.append({
            "search_id": search[0],
            "search_query": search[1],
            "result_count": search[2],
            "search_date": search[3],
            "recommended_courses": [
                {"course_title": course[0], "course_id": course[1], "campus": course[2]}
                for course in recommended_courses
            ]
        })

    close_connection(db)
    return history

def clear_search_history(user_id):
    db = create_connection()
    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM RecommendedCourses WHERE user_id = %s
    """, (user_id,))
    cursor.execute("""
        DELETE FROM UserSearchHistory WHERE user_id = %s
    """, (user_id,))
    db.commit()
    close_connection(db)
    return {"message": "Your search history has been cleared."}