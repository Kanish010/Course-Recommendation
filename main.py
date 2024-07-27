from course_recommendation import recommend_courses
from auth import register_user, authenticate_user
from database import create_connection, close_connection

def main_menu(user_id):
    while True:
        print("\nMenu:")
        print("1. Perform a new search")
        print("2. View and Manage Search History")
        print("3. Set or update preferences")
        print("4. Manage Favorites")
        print("5. Logout")
        choice = input("Please select an option (1-5): ").strip()
        
        if choice == '1':
            new_search(user_id)
        elif choice == '2':
            manage_search_history(user_id)
        elif choice == '3':
            set_user_preferences(user_id)
        elif choice == '4':
            manage_favorites(user_id)
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

def manage_favorites(user_id):
    while True:
        print("\nManage Favorites:")
        print("1. View favorite courses")
        print("2. Add a course to favorites")
        print("3. Remove a course from favorites")
        print("4. Back to main menu")
        choice = input("Please select an option (1-4): ").strip()
        
        if choice == '1':
            view_favorites(user_id)
        elif choice == '2':
            add_to_favorites(user_id)
        elif choice == '3':
            remove_from_favorites(user_id)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please select a valid option.")

def view_favorites(user_id):
    db = create_connection()
    cursor = db.cursor()
    cursor.execute("""
        SELECT `Courses`.`Course ID`, `Courses`.`Course Title`, `Courses`.`Campus`
        FROM FavoriteCourses
        JOIN Courses ON FavoriteCourses.course_id = Courses.`Course ID`
        WHERE FavoriteCourses.user_id = %s
    """, (user_id,))
    favorites = cursor.fetchall()
    
    if favorites:
        print("\nYour Favorite Courses:")
        for course in favorites:
            print(f"{course[0]}: {course[1]} (Campus: {course[2]})")
    else:
        print("You have no favorite courses.")
    close_connection(db)

def add_to_favorites(user_id):
    print("Please enter the Course ID in the format 'MGMT_O 450'.")
    course_id = input("Enter the Course ID of the course you want to add to favorites: ").strip()
    
    db = create_connection()
    cursor = db.cursor()
    cursor.execute("SELECT `Course ID` FROM Courses WHERE `Course ID` = %s", (course_id,))
    course = cursor.fetchone()
    
    if course:
        cursor.execute("""
            INSERT INTO FavoriteCourses (user_id, course_id)
            VALUES (%s, %s)
        """, (user_id, course_id))
        db.commit()
        print(f"Course {course_id} has been added to your favorites.")
    else:
        print("Invalid Course ID. Please try again.")
    close_connection(db)

def remove_from_favorites(user_id):
    print("Please enter the Course ID in the format 'MGMT_O 450'.")
    course_id = input("Enter the Course ID of the course you want to remove from favorites: ").strip()
    
    db = create_connection()
    cursor = db.cursor()
    cursor.execute("""
        DELETE FROM FavoriteCourses
        WHERE user_id = %s AND course_id = %s
    """, (user_id, course_id))
    db.commit()
    
    if cursor.rowcount > 0:
        print(f"Course {course_id} has been removed from your favorites.")
    else:
        print("Course not found in your favorites. Please check the Course ID and try again.")
    close_connection(db)

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

    # Delete all entries related to the user's search history
    cursor.execute("""
        DELETE FROM RecommendedCourses WHERE user_id = %s
    """, (user_id,))
    cursor.execute("""
        DELETE FROM UserSearchHistory WHERE user_id = %s
    """, (user_id,))
    db.commit()
    close_connection(db)
    print("Your search history has been cleared.")

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

def main():
    while True:
        action = input("Do you want to [R]egister or [L]ogin? (E to Exit) ").strip().lower()
        if action == 'r':
            username = input("Enter a username: ").strip()
            email = input("Enter your email: ").strip()
            password = input("Enter a password: ").strip()
            
            user_id = register_user(username, email, password)
            if user_id is None:
                continue
            print(f"User {username} registered successfully")
        elif action == 'l':
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            
            user_id = authenticate_user(username, password)
            if user_id is None:
                continue
            print(f"User {username} authenticated successfully")

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

        main_menu(user_id)

if __name__ == "__main__":
    main()