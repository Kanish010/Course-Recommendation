from database import create_connection, close_connection

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
    print("Please enter the Course ID in the format 'MGMT_O 450' for Okanagan or 'CPSC_V 322' for Vancouver.")
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
    print("Please enter the Course ID in the format 'MGMT_O 450' for Okanagan or 'CPSC_V 322' for Vancouver.")
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