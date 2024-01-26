
# Mountain Project Scraper and Data Organizer

A MountainProject.com web scraper and data organizer.

## Description

This web scraper will collect area and route data across mountain project. This data can then be uploaded to a SQL database for further data exploration. 

## Getting Started:
### Dependencies

Dependencies are outlined in the requirements.txt file as well as below:
* Python 3.8.8 
* Scrapy 2.10.1 
* Pandas 1.2.4

### Installing
To clone this repository to your local machine, follow these steps:
1. Open your terminal and navigate to where you want to clone the repository
2. Use the following Git command to clone the repository:
```
git clone https://github.com/tayloraportman/MtnProject.git
```
3. Change to the repository directory:
```
cd MtnProject
```
4. To pull the latest updates or changes from the repository, use:
```
git pull origin main
```
### Executing program
* To execute the spider run the following command:
```
scrapy crawl mtnspider 

```
* If you would like to test the spider before running it in full, run the parser with a limited pagecount. This will allow you to see if the parser logic is working without scraping from the entire website. 
To execute the spider with limited pagecount, use the following command:
```
scrapy crawl mtnspider -s CLOSESPIDER_PAGECOUNT=20

```
**All scraped data will be cleaned and stored in the SQL database associated with the spider** 
per the pipelines.py file

* To open the associated database, run the following command:
```
sqlite3 mtnspider_json.db
```
**The database contains three main tables, AreaData, RouteData, and StatData**
**AreaData** contains information about various areas, with each record including details such as:

- `elevation_ft`: Elevation of the area in feet.
- `GPS`: GPS coordinates of the area.
- `area_name`: Name of the area.
- `state_name`: Name of the state where the area is located.
- `area_id`: A unique identifier for the area.

**RouteData** contains information about different climbing routes, with each record including details such as:

- `climb_type`: Type of the climb (e.g., Boulder).
- `climb_height_ft` and `climb_height_m`: Height of the climb in feet and meters.
- `first_ascent`: The name of the person who first ascended the route.
- `page_views_total` and `page_views_per_month`: Total and monthly page views for the route.
- `gradeYDS` and `gradeFont`: Climbing difficulty grades in the YDS (Yosemite Decimal System) and Fontainebleau grading systems.
- `state_name`: Name of the state where the climb is located.
- `area_id` and `area_name`: Identifier and name of the area where the route is located.
- `route_id` and `route_name`: Identifier and name of the route.

**StatData** contains statistical data related to climbing routes, with each record including:

- `route_id`: A unique identifier for the climbing route.
- `avg_stars`: The average star rating given to the route.
- `num_votes`: The number of votes or ratings the route has received.

For example, the first record corresponds to the route with ID `108516795`, which has an average star rating of 0.0 based on 0 votes.

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Taylor A Portman



