CREATE DATABASE IF NOT EXISTS CourseRecommendationDB;
USE CourseRecommendationDB;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE UserPreferences (
    user_id INT PRIMARY KEY,
    preferred_levels VARCHAR(50),
    interests TEXT,
    preferred_campus VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE UserSearchHistory (
    search_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    search_query VARCHAR(255),
    search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    result_count INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Courses (
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