from Features.registration_login import handle_registration, handle_login
from Features.favorites import manage_favorites
from Features.search import new_search, perform_search
from Features.search_history import manage_search_history
from Features.rate_courses import manage_ratings
from Features.set_preferences import set_user_preferences

def main_menu(user_id):
    while True:
        print("\nMenu:")
        print("1. Perform a new search")
        print("2. View and Manage Search History")
        print("3. Set or update preferences")
        print("4. Manage Favorites")
        print("5. Manage Course Ratings")
        print("6. Logout")
        choice = input("Please select an option (1-6): ").strip()
        
        if choice == '1':
            new_search(user_id)
        elif choice == '2':
            manage_search_history(user_id)
        elif choice == '3':
            set_user_preferences(user_id)
        elif choice == '4':
            manage_favorites(user_id)
        elif choice == '5':
            manage_ratings(user_id)
        elif choice == '6':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

def main():
    while True:
        action = input("Do you want to [R]egister or [L]ogin? (E to Exit) ").strip().lower()
        if action == 'r':
            user_id = handle_registration()
            if user_id:
                main_menu(user_id)
        elif action == 'l':
            user_id = handle_login()
            if user_id:
                main_menu(user_id)
        elif action == 'e':
            print("Exiting program.")
            return
        else:
            print("Invalid action.")
            continue

if __name__ == "__main__":
    main()