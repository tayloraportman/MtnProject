# %%
import sqlite3
import json

# Create a SQLite database (or connect to an existing one)
conn = sqlite3.connect('mountain_project_data.db')
cursor = conn.cursor()

# Create a table for area data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS area_data (
        area_id INTEGER PRIMARY KEY,
        area_name TEXT,
        state_name TEXT,
        elevation_ft INTEGER,
        GPS TEXT
    )
''')

# Create a table for route data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS route_data (
        route_id INTEGER PRIMARY KEY,
        area_id INTEGER,
        route_name TEXT,
        state_name TEXT,
        climb_type TEXT,
        climb_height_ft INTEGER,
        climb_height_m INTEGER,
        first_ascent TEXT,
        page_views_total INTEGER,
        page_views_per_month INTEGER,
        gradeYDS TEXT,
        gradeFont TEXT
    )
''')

# Create a table for route statistics
cursor.execute('''
    CREATE TABLE IF NOT EXISTS route_stats (
        route_id INTEGER PRIMARY KEY,
        avg_stars REAL,
        num_votes INTEGER
    )
''')

# Load and insert data into the area_data table
with open('V6_area_data.json', 'r') as json_file:
    area_data = json.load(json_file)
    for entry in area_data:
        cursor.execute('''
            INSERT INTO area_data (area_id, area_name, state_name, elevation_ft, GPS)
            VALUES (?, ?, ?, ?, ?)
        ''', (entry['area_id'], entry['area_name'], entry['state_name'], entry.get('elevation_ft'), entry.get('GPS')))

# Load and insert data into the route_data table
with open('V6_route_data.json', 'r') as json_file:
    route_data = json.load(json_file)
    for entry in route_data:
        cursor.execute('''
            INSERT INTO route_data (route_id, area_id, route_name, state_name, climb_type, climb_height_ft,
            climb_height_m, first_ascent, page_views_total, page_views_per_month, gradeYDS, gradeFont)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (entry['route_id'], entry['area_id'], entry['route_name'], entry['state_name'], entry.get('climb_type'),
              entry.get('climb_height_ft'), entry.get('climb_height_m'), entry.get('first_ascent'),
              entry.get('page_views_total'), entry.get('page_views_per_month'), entry.get('gradeYDS'), entry.get('gradeFont')))

# Load and insert data into the route_stats table
with open('V6_stat_data.json', 'r') as json_file:
    stat_data = json.load(json_file)
    for entry in stat_data:
        cursor.execute('''
            INSERT INTO route_stats (route_id, avg_stars, num_votes)
            VALUES (?, ?, ?)
        ''', (entry['route_id'], entry['avg_stars'], entry['num_votes']))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data inserted into the database successfully.")



