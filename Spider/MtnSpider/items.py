# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# Based on the provided information, let's create the definitions for the Scrapy items in items.py

from scrapy import Item, Field

# Define the AreaData item
class AreaDataItems(Item):
    elevation_ft = Field()  # Elevation of the area in feet
    GPS = Field()           # GPS coordinates of the area
    area_name = Field()     # Name of the area
    state_name = Field()    # Name of the state where the area is located
    area_id = Field()       # Unique identifier for the area

# Define the RouteData item
class RouteDataItems(Item):
    climb_type = Field()            # Type of the climb (e.g., Boulder)
    climb_height_ft = Field()       # Height of the climb in feet
    climb_height_m = Field()        # Height of the climb in meters
    num_pitches = Field()           # Number of pitches
    first_ascent = Field()          # Name of the person who first ascended the route
    page_views_total = Field()      # Total page views for the route
    page_views_per_month = Field()  # Monthly page views for the route
    gradeYDS = Field()              # Climbing difficulty grade in YDS system
    gradeFont = Field()             # Climbing difficulty grade in Fontainebleau system
    state_name = Field()            # Name of the state where the climb is located
    area_id = Field()               # Identifier of the area where the route is located
    area_name = Field()             # Name of the area where the route is located
    route_id = Field()              # Identifier of the route
    route_name = Field()            # Name of the route

# Define the StatData item
class StatDataItems(Item):
    route_id = Field()    # Unique identifier for the climbing route
    avg_stars = Field()   # Average star rating given to the route
    num_votes = Field()   # Number of votes or ratings the route has received

# These class definitions should be placed in your items.py file. 
# They will define the structure of the data that your spider will be scraping and passing to the pipeline.



