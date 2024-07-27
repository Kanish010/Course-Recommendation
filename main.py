from course_recommendation import recommend_courses
from auth import register_user, authenticate_user
from database import create_connection, close_connection

def main():
    while True:
        # Prompt for user credentials
        action = input("Do you want to [R]egister or [L]ogin? (E to Exit) ").strip().lower()
        if action == 'r':
            username = input("Enter a username: ").strip().lower()
            email = input("Enter your email: ").strip().lower()
            password = input("Enter a password: ").strip()
            
            user_id = register_user(username, email, password)
            if user_id is None:
                continue
            print(f"User {username} registered successfully")
        elif action == 'l':
            username = input("Enter your username: ").strip().lower()
            password = input("Enter your password: ").strip()
            
            user_id = authenticate_user(username, password)
            if user_id is None:
                continue
            print(f"User {username} authenticated successfully")

            # Check for last search and offer to continue
            db = create_connection()
            cursor = db.cursor()
            cursor.execute("""
                SELECT preferred_levels, interests, preferred_campus
                FROM UserLastSearch WHERE user_id = %s
            """, (user_id,))
            last_search = cursor.fetchone()
            close_connection(db)

            if last_search:
                levels, last_interest, last_campus = last_search
                resume = input(f"Do you want to continue with your last search: Interest='{last_interest}', Levels='{levels}', Campus='{last_campus}'? (Y/N): ").strip().lower()
                if resume == 'y':
                    campus = last_campus
                    user_interest = last_interest
                    levels_str = levels
                    levels = levels_str.split(',') if levels_str != "All Levels" else ["All Levels"]
                    levels = [level.strip() for level in levels]
                    perform_search(user_id, campus, user_interest, levels)
                else:
                    last_search = None
        elif action == 'e':
            print("Exiting program.")
            return
        else:
            print("Invalid action.")
            continue

        # Main menu loop
        while True:
            print("\nMenu:")
            print("1. Perform a new search")
            print("2. View previous searches")
            print("3. View favorite courses")
            print("4. Set or update preferences")
            print("5. Logout")
            choice = input("Please select an option (1, 2, 3, 4, 5): ").strip()
            
            if choice == '1':
                # Prompt for new search criteria
                campus = input("Which campus are you interested in? (Okanagan/Vancouver): ").strip().lower().replace(" ", "")
                if campus not in ['okanagan', 'vancouver']:
                    print("Invalid campus selection. Please enter 'Okanagan' or 'Vancouver'.")
                    continue

                user_interest = input("Please describe your area of interest: ").strip()
                if not user_interest:
                    print("You did not provide an area of interest.")
                    continue
                
                user_levels_input = input("Which course levels are you interested in? (100, 200, ..., 700, leave blank for all levels): ").strip().replace(" ", "")
                levels = user_levels_input.split(',') if user_levels_input else ["All Levels"]
                levels = [level.strip() for level in levels if level.strip() in {'100', '200', '300', '400', '500', '600', '700'}]

                # Perform the new search
                perform_search(user_id, campus, user_interest, levels)

            elif choice == '2':
                # View previous searches
                view_previous_searches(user_id)

            elif choice == '3':
                # View favorite courses
                view_favorite_courses(user_id)

            elif choice == '4':
                # Set or update preferences
                set_user_preferences(user_id)

            elif choice == '5':
                print("Logging out...")
                break

            else:
                print("Invalid choice. Please select a valid option.")

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

    levels_to_use = [] if levels == ["All Levels"] else levels
    recommended_courses = recommend_courses(campus, user_interest, levels_to_use)
    
    result_count = len(recommended_courses) if not recommended_courses.empty else 0
    if result_count > 0:
        print("\nRecommended courses for you:")
        print(recommended_courses.to_string(index=False))
    else:
        print(f"\nNo {', '.join(levels)} level courses with interest '{user_interest}' were found.")

    # Log the search in UserSearchHistory
    cursor.execute("""
        INSERT INTO UserSearchHistory (user_id, search_query, result_count)
        VALUES (%s, %s, %s)
    """, (user_id, f"Interest: {user_interest}, Levels: {levels_str}", result_count))
    db.commit()

    # Get the search_id of the last inserted search
    search_id = cursor.lastrowid

    # Log recommended courses
    for _, row in recommended_courses.iterrows():
        cursor.execute("""
            INSERT INTO RecommendedCourses (search_id, course_title, course_id, campus)
            VALUES (%s, %s, %s, %s)
        """, (search_id, row['Course Title'], row['Course ID'], campus))
    db.commit()

    close_connection(db)

def view_previous_searches(user_id):
    db = create_connection()
    if db is None:
        print("Failed to connect to the database. Please try again later.")
        return

    cursor = db.cursor()
    cursor.execute("""
        SELECT search_id, search_query, result_count, search_date
        FROM UserSearchHistory
        WHERE user_id = %s
        ORDER BY search_date DESC
    """, (user_id,))
    searches = cursor.fetchall()

    if searches:
        print("\nPrevious Searches:")
        for search in searches:
            print(f"\nSearch Query: {search[1]}")
            print(f"Results Found: {search[2]}")
            print(f"Date: {search[3]}")

            # Fetch recommended courses for this search
            cursor.execute("""
                SELECT course_title, course_id
                FROM RecommendedCourses
                WHERE search_id = %s
            """, (search[0],))
            recommended_courses = cursor.fetchall()

            if recommended_courses:
                print("Recommended Courses:")
                for course in recommended_courses:
                    print(f"- {course[0]} (Course ID: {course[1]})")
            else:
                print("No recommended courses found for this search.")

    else:
        print("No previous searches found.")

    close_connection(db)

def view_favorite_courses(user_id):
    db = create_connection()
    cursor = db.cursor()
    cursor.execute("""
        SELECT course_id FROM FavoriteCourses
        WHERE user_id = %s
    """, (user_id,))
    favorite_courses = cursor.fetchall()
    close_connection(db)
    
    if favorite_courses:
        print("\nFavorite Courses:")
        for course in favorite_courses:
            print(f"Course ID: {course[0]}")
    else:
        print("No favorite courses found.")

def set_user_preferences(user_id):
    preferred_levels_input = input("Enter your preferred course levels (e.g., 100, 200, 300, leave blank for all): ").strip()
    preferred_levels = preferred_levels_input if preferred_levels_input else "All Levels"
    interests = input("Enter your interests (comma separated): ").strip()
    preferred_campus = input("Enter your preferred campus (Okanagan/Vancouver): ").strip()

    db = create_connection()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO UserPreferences (user_id, preferred_levels, interests, preferred_campus)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE preferred_levels=%s, interests=%s, preferred_campus=%s
    """, (user_id, preferred_levels, interests, preferred_campus, preferred_levels, interests, preferred_campus))
    db.commit()
    close_connection(db)
    print("Preferences updated successfully.")

if __name__ == "__main__":
    main()