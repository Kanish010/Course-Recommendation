from auth import register_user, authenticate_user
from database import create_connection, close_connection

def handle_registration(data):
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    user_id = register_user(username, email, password)
    if user_id is None:
        return None
    else:
        return user_id

def handle_login(data):
    username = data.get('username')
    password = data.get('password')
    
    user_id = authenticate_user(username, password)
    if user_id is None:
        db = create_connection()
        cursor = db.cursor()
        cursor.execute("SELECT username FROM Users WHERE username = %s", (username,))
        if cursor.fetchone():
            close_connection(db)
            return {'success': False, 'message': 'Password is incorrect. Please try again.'}
        else:
            close_connection(db)
            return {'success': False, 'message': 'Username does not exist. Please register.'}
    else:
        return {'success': True, 'user_id': user_id}