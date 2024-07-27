import os

DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://username:password@localhost/CourseRecommendationDB')
SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')