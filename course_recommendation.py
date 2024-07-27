import mysql.connector
from database import create_connection, close_connection
import re

def recommend_courses(cursor, campus, interest, levels):
    # Base query
    base_query = """
    SELECT `Course ID`, `Course Title`
    FROM Courses
    WHERE Campus = %s AND
    (`Course Description` LIKE %s OR `Course Title` LIKE %s)
    """
    
    params = [campus, f"%{interest}%", f"%{interest}%"]

    # Handle levels filtering
    if levels and levels[0] != "All Levels":
        level_conditions = []
        for level in levels:
            if level.isdigit():
                level_range_start = int(level)
                level_range_end = level_range_start + 99
                # Extract the numeric part of `Course ID` and filter by level range
                level_conditions.append(f"""
                CAST(SUBSTRING_INDEX(SUBSTRING(`Course ID`, LENGTH(`Course ID`) - 3), ' ', -1) AS UNSIGNED) BETWEEN {level_range_start} AND {level_range_end}
                """)
        
        if level_conditions:
            base_query += " AND (" + " OR ".join(level_conditions) + ")"

    cursor.execute(base_query, params)
    return cursor.fetchall()