CREATE DATABASE IF NOT EXISTS CourseRecommendationDB;
USE CourseRecommendationDB;

-- Users Table
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- UserLastSearch Table
CREATE TABLE IF NOT EXISTS UserLastSearch (
    user_id INT PRIMARY KEY,
    preferred_levels VARCHAR(50),
    interests TEXT,
    preferred_campus VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- UserSearchHistory Table
CREATE TABLE IF NOT EXISTS UserSearchHistory (
    search_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    search_query VARCHAR(255),
    search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    result_count INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- RecommendedCourses Table
CREATE TABLE RecommendedCourses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    course_title VARCHAR(255),
    course_id VARCHAR(50),
    campus VARCHAR(50),
    search_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (search_id) REFERENCES UserSearchHistory(search_id)
);

-- Courses Table
CREATE TABLE IF NOT EXISTS Courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    course_title VARCHAR(255) NOT NULL,
    course_description TEXT,
    course_level VARCHAR(50),
    course_credits INT,
    campus VARCHAR(50),
    department VARCHAR(100),
    professor VARCHAR(100)
);

-- UserPreferences Table
CREATE TABLE IF NOT EXISTS UserPreferences (
    user_id INT PRIMARY KEY,
    preferred_levels VARCHAR(50),
    interests TEXT,
    preferred_campus VARCHAR(50),
    notifications_enabled BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- FavoriteCourses Table
CREATE TABLE IF NOT EXISTS FavoriteCourses (
    user_id INT,
    course_id VARCHAR(50),
    PRIMARY KEY (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- CourseRatings Table
CREATE TABLE CourseRatings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_id VARCHAR(255) NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    UNIQUE KEY unique_user_course (user_id, course_id(255))
);