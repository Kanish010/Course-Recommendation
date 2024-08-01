from database import create_connection, close_connection

def manage_ratings(user_id):
    while True:
        print("\nManage Course Ratings:")
        print("1. Rate a course")
        print("2. View your ratings")
        print("3. Update a rating")
        print("4. Delete a rating")
        print("5. Back to main menu")
        choice = input("Please select an option (1-5): ").strip()
        
        if choice == '1':
            rate_course(user_id)
        elif choice == '2':
            view_ratings(user_id)
        elif choice == '3':
            update_rating(user_id)
        elif choice == '4':
            delete_rating(user_id)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please select a valid option.")

def rate_course(user_id):
    print("Please enter the Course ID in the format 'MGMT_O 450' for Okanagan or 'CPSC_V 322' for Vancouver.")
    course_id = input("Enter the Course ID of the course you want to rate: ").strip()
    rating = int(input("Enter your rating for the course (1 to 5): ").strip())

    db = create_connection()
    cursor = db.cursor()
    
    # Check if the user has already rated the course
    cursor.execute("""
        SELECT * FROM CourseRatings WHERE user_id = %s AND course_id = %s
    """, (user_id, course_id))
    existing_rating = cursor.fetchone()
    
    if existing_rating:
        print("You have already rated this course. Please update your rating if you want to change it.")
    else:
        cursor.execute("""
            INSERT INTO CourseRatings (user_id, course_id, rating)
            VALUES (%s, %s, %s)
        """, (user_id, course_id, rating))
        db.commit()
        print(f"Your rating of {rating} has been added for the course {course_id}.")

    close_connection(db)

def view_ratings(user_id):
    db = create_connection()
    cursor = db.cursor()
    cursor.execute("SELECT course_id, rating FROM CourseRatings WHERE user_id = %s", (user_id,))
    ratings = cursor.fetchall()
    close_connection(db)
    
    if ratings:
        print("\nYour Ratings:")
        for rating in ratings:
            print(f"Course ID: {rating[0]}, Rating: {rating[1]}")
    else:
        print("You have not rated any courses yet.")

def update_rating(user_id):
    print("Please enter the Course ID in the format 'MGMT_O 450' for Okanagan or 'CPSC_V 322' for Vancouver.")
    course_id = input("Enter the Course ID of the rating you want to update: ").strip()
    new_rating = input("Enter your new rating (1-5): ").strip()
    
    db = create_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE CourseRatings SET rating = %s WHERE user_id = %s AND course_id = %s", (new_rating, user_id, course_id))
    db.commit()
    close_connection(db)
    print(f"Rating for course {course_id} has been updated to {new_rating}.")

def delete_rating(user_id):
    print("Please enter the Course ID in the format 'MGMT_O 450' for Okanagan or 'CPSC_V 322' for Vancouver.")
    course_id = input("Enter the Course ID of the rating you want to delete: ").strip()
    
    db = create_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM CourseRatings WHERE user_id = %s AND course_id = %s", (user_id, course_id))
    db.commit()
    close_connection(db)
    print(f"Rating for course {course_id} has been deleted.")