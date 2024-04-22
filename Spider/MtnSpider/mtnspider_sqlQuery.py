from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import AreaData, RouteData, StatData
import csv

# Define the SQLAlchemy database URI
DATABASE_URI = 'sqlite:///mtnspider_database.db'

# Specify the path to the CSV file
csv_file_path = 'combined_data_all.csv'

# Create the database engine
engine = create_engine(DATABASE_URI)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Define a query to join the AreaData, RouteData, and stat_data tables
query = session.query(
    AreaData.area_id, AreaData.elevation_ft, AreaData.GPS, AreaData.area_name, AreaData.state_name,
    RouteData.route_id, RouteData.climb_type, RouteData.climb_height_ft, RouteData.climb_height_m,
    RouteData.num_pitches, RouteData.first_ascent, RouteData.page_views_total, RouteData.page_views_per_month,
    RouteData.gradeYDS, RouteData.gradeFont,
    StatData.avg_stars, StatData.num_votes
).join(RouteData, AreaData.area_id == RouteData.area_id
).join(StatData, RouteData.route_id == StatData.route_id)

# Fetch all results
results = query.all()

# Check that the first 5 results are correct
for result in results[:5]:
    print(result)


# Write data to CSV
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the headers
    writer.writerow([
        'Area ID', 'Elevation (ft)', 'GPS', 'Area Name', 'State Name',
        'Route ID', 'Climb Type', 'Climb Height (ft)', 'Climb Height (m)',
        'Number of Pitches', 'First Ascent', 'Total Page Views', 'Page Views per Month',
        'Grade YDS', 'Grade Font',
        'Average Stars', 'Number of Votes'
    ])
    # Write the data rows
    for row in results:
        writer.writerow(row)

# Close the session
session.close()

print(f"Data successfully written to {csv_file_path}")
