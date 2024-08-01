from database import create_connection, close_connection

def manage_search_history(user_id):
    while True:
        print("\nManage Search History:")
        print("1. View previous searches")
        print("2. Clear entire search history")
        print("3. Back to main menu")
        choice = input("Please select an option (1-3): ").strip()
        
        if choice == '1':
            view_previous_searches(user_id)
        elif choice == '2':
            clear_search_history(user_id)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please select a valid option.")

def view_previous_searches(user_id):
    db = create_connection()
    if db is None:
        print("Failed to connect to the database. Please try again later.")
        return

    cursor = db.cursor()
    cursor.execute("""
        SELECT search_query, result_count, search_date
        FROM UserSearchHistory
        WHERE user_id = %s
        ORDER BY search_date DESC
    """, (user_id,))
    searches = cursor.fetchall()

    if searches:
        print("\nPrevious Searches:")
        for index, search in enumerate(searches):
            print(f"\n{index + 1}. Search Query: {search[0]}")
            print(f"   Results Found: {search[1]}")
            print(f"   Date: {search[2]}")
            cursor.execute("""
                SELECT course_title, course_id, campus
                FROM RecommendedCourses
                WHERE user_id = %s
            """, (user_id,))
            recommended_courses = cursor.fetchall()

            if recommended_courses:
                print("   Recommended Courses:")
                for course in recommended_courses:
                    print(f"   - {course[0]} (Course ID: {course[1]}, Campus: {course[2]})")
            else:
                print("   No recommended courses found for this search.")
    else:
        print("No previous searches found.")

    close_connection(db)

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
    print("Your search history has been cleared.")