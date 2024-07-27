from course_recommendation import recommend_courses
from database import create_connection, close_connection
from auth import register_user, authenticate_user

def main():
    # Initialize database connection
    db = create_connection()

    # Example user registration and authentication flow
    username = "example_user"
    email = "example_user@example.com"
    password = "example_password"
    
    # Register a new user
    register_user(username, email, password)
    
    # Authenticate the user
    if authenticate_user(username, password):
        print(f"User {username} authenticated successfully")
        
        # User input for campus, interest, and levels
        valid_levels = {'100', '200', '300', '400', '500', '600', '700'}
        
        while True:
            campus = input("Which campus are you interested in? (Okanagan/Vancouver): ").strip().lower().replace(" ", "")
            if campus in ['okanagan', 'vancouver']:
                break
            else:
                print("Invalid campus selection. Please enter 'Okanagan' or 'Vancouver'.")
        
        user_interest = input("Please describe your area of interest: ").strip()
        if not user_interest:
            print("You did not provide an area of interest.")
            return
        
        while True:
            user_levels_input = input("Which course levels are you interested in? (100, 200, ..., 700, leave blank for all levels): ").strip().replace(" ", "")
            if user_levels_input:
                levels = user_levels_input.split(',')
                if all(level in valid_levels for level in levels):
                    break
                else:
                    print("Please enter valid course levels (100, 200, ..., 700) or leave blank for all levels.")
            else:
                levels = list(valid_levels)
                break
        
        # Call the course recommendation function
        recommended_courses = recommend_courses(campus, user_interest, levels)
        
        if not recommended_courses.empty:
            print("\nRecommended courses for you:")
            print(recommended_courses.to_string(index=False))
        else:
            print(f"\nNo {', '.join(levels)} level courses with interest '{user_interest}' were found.")
    else:
        print("Authentication failed")

    # Close the database connection
    close_connection(db)

if __name__ == "__main__":
    main()