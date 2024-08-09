from flask import Flask, request, jsonify
from flask_cors import CORS
from Features.registration_login import handle_registration, handle_login
from Features.favorites import manage_favorites
from Features.search import new_search, perform_search
from Features.search_history import get_search_history, clear_search_history
from Features.rate_courses import manage_ratings
from Features.set_preferences import set_user_preferences

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    user_id = handle_registration(data)
    if user_id:
        return jsonify({'success': True, 'user_id': user_id})
    else:
        return jsonify({'success': False, 'message': 'Registration failed'}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    result = handle_login(data)
    if result['success']:
        return jsonify({'success': True, 'user_id': result['user_id']})
    else:
        return jsonify({'success': False, 'message': result['message']}), 400

@app.route('/api/search-history', methods=['POST'])
def search_history():
    data = request.json
    user_id = data['user_id']
    print(f"Received request for search history with user_id: {user_id}")
    
    history = get_search_history(user_id)
    print(f"Search history returned: {history}")

    if isinstance(history, dict) and "error" in history:
        print(f"Error in search history retrieval: {history['error']}")
        return jsonify({"success": False, "message": history["error"]})

    return jsonify({"success": True, "history": history})

@app.route('/api/clear-search-history', methods=['POST'])
def clear_history():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"success": False, "message": "No user_id provided."}), 400

    result = clear_search_history(user_id)
    return jsonify({"success": True, "message": result["message"]})

@app.route('/api/preferences', methods=['POST'])
def preferences():
    data = request.json
    user_id = data['user_id']
    preferences = set_user_preferences(user_id)
    return jsonify(preferences)

@app.route('/api/favorites', methods=['POST'])
def favorites():
    data = request.json
    user_id = data['user_id']
    favorites = manage_favorites(user_id)
    return jsonify(favorites)

@app.route('/api/ratings', methods=['POST'])
def ratings():
    data = request.json
    user_id = data['user_id']
    ratings = manage_ratings(user_id)
    return jsonify(ratings)

if __name__ == '__main__':
    app.run(debug=True)