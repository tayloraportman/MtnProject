# %% [markdown]
# Mountain Project scraper
# Taylor Portman
# January 10, 2024

# %%
import scrapy
import pandas as pd
import json
import logging
import re
from scrapy.downloadermiddlewares.retry import RetryMiddleware

class MtnSpider(scrapy.Spider):
    name = 'mtnspider'
    start_urls = ['https://www.mountainproject.com/']
    area_data = []
    route_data = []
    stat_data = []

    custom_settings = {
        'DOWNLOAD_DELAY': 0.002, #avoid overloading the server with too many requests in a short period.
        'RETRY_HTTP_CODES': [429], #This specifies that the spider should retry requests that result in HTTP status code 429 (Too Many Requests)
        'RETRY_TIMES': 3,
        'USER_AGENTS': [ #The user-agent strings are simulated as if the requests are coming from different web browsers
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        ],
    }

    # Parser 1: Collect by states + international + in progress from moutainproject homepage
    def parse(self, response):
        # Parse states and collect their URLs
        state_urls = response.css('#route-guide > div:nth-child(n) > div:nth-child(n) > strong > div > div:nth-child(n) > a::attr(href)').extract()
        state_name = response.css('#route-guide > div:nth-child(n) > div:nth-child(n) > strong > div > div:nth-child(n) > a::text').extract()

        for state_name, state_url in zip(state_name, state_urls): 
                    # Send requests for state-specific pages while passing state_name as a meta parameter
            yield scrapy.Request(url=state_url, callback=self.parse_areas, meta={'state_name': state_name})

    def handle_request_error(self, failure):
        # Handle request errors here
        self.logger.error(f"Request error: {failure}")

    # Parser 2: For each state: IF areas/ sub areas collect urls and save identifier
    def parse_areas(self, response):
        state_name = response.meta.get('state_name')
        title = response.css('#climb-area-page > div > div.col-md-3.left-nav.float-md-left.mb-2 > div > h3::text').get()
        area_info_raw = response.css('#climb-area-page table tr td::text').extract()
        cleaned_text_area = ' '.join(map(str.strip, area_info_raw))
        area_id = None  # Initialize area_id with a default value
        route_id = None # Initialize route_id with a default value

        if title is not None and title.startswith("Areas"):
            area_urls = response.css('#climb-area-page > div > div.col-md-3.left-nav.float-md-left.mb-2 > div > div.max-height.max-height-md-0.max-height-xs-400 > div:nth-child(n) > a::attr(href)').extract()
            area_name = response.css('#climb-area-page > div > div.col-md-3.left-nav.float-md-left.mb-2 > div > div.max-height.max-height-md-0.max-height-xs-400 > div:nth-child(n) > a::text').extract()

            for area_url in area_urls:
                match_area = re.search(r'area/(\d+)', area_url)
                if match_area:
                    area_id = match_area.group(1)
                    yield {'area_id': area_id}
                else:
                    self.logger.warning("match_area pattern not found")

                for url, name in zip(area_urls, area_name):
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse_areas,
                        meta={'state_name': state_name, 'area_name': name, 'area_id': area_id}
                    )

        elif title is not None and title.startswith("Routes"): #For each area collect routes and forward to parse_routes
            area_id = response.meta['area_id']
            area_name = response.meta['area_name']
            route_urls = response.css('#left-nav-route-table td:nth-child(n) a::attr(href)').extract()

            for route_url in route_urls:
                match_route = re.search(r'route/(\d+)', route_url)
                if match_route:
                    route_id = match_route.group(1)
                    yield {'route_id': route_id}
                else:
                    self.logger.warning("match_route pattern not found")

                route_name = response.css('#left-nav-route-table td:nth-child(n) a::text').extract()
    
                for url, name in zip(route_urls, route_name):
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse_routes,
                        meta={'state_name': state_name, 'area_name': area_name, 'route_name': name, 'area_id': area_id, 'route_id': route_id}
                    )
        else: 
            self.logger.warning("Title element not found")

        ### Extract data from area page ###
        # Define regular expressions and corresponding field names
        patterns = [
             (r'Elevation:\s*([\d,]+)\s*ft', 'elevation_ft'),    # Match and extract route elevation
             (r'GPS:\s*(-?[\d.]+,\s*-?[\d.]+)', 'GPS')                        # Match and extract GPS data
             ]

        area_data = {}
        
        for pattern, field in patterns:
            match = re.search(pattern, cleaned_text_area)
            if match:
                area_data[field] = match.group(1).strip()
            else:
                    self.logger.warning("area_data pattern not found")

        yield area_data

        area_data['area_name'] = response.meta['area_name']
        area_data['state_name'] = response.meta['state_name']
        area_data['area_id'] = response.meta['area_id']
       

        self.area_data.append(area_data) 

    # Parser 3: For each area/ sub area: IF route then collect data
    def parse_routes(self, response):
        # Extract YDS grade
        gradeYDS = response.css('#route-page > div > div.col-md-9.float-md-right.mb-1 > h2 > span.rateYDS::text').extract()
        gradeYDS = gradeYDS[0] if gradeYDS else None

        # Extract Font grade
        gradeFont = response.css('#route-page > div > div.col-md-9.float-md-right.mb-1 > h2 > span.rateFont::text').extract()
        gradeFont = gradeFont[0] if gradeFont else None

        # Extract route information
        page_info_raw = response.css('#route-page table tr td::text').extract()
        cleaned_text = ' '.join(map(str.strip, page_info_raw))

        # Define regular expressions and corresponding field names
        patterns = [
            (r'Type:\s*([A-Za-z]+)', 'climb_type'),                   # Match and extract climb type
            (r'(\d+)\s*ft', 'climb_height_ft'),                       # Match and extract climb height in feet
            (r'\((\d+)\s*m\)', 'climb_height_m'),                     # Match and extract climb height in meters
            (r'FA:\s*([^:]+)(?= Page Views:|$)', 'first_ascent'),     # Match and extract First Ascent information
            (r'Page Views:\s*([\d,]+)', 'page_views_total'),           # Match and extract total page views
            (r'(\d+)/month', 'page_views_per_month')                  # Match and extract page views per month
        ]

        route_data = {}

        for pattern, field in patterns:
            match = re.search(pattern, cleaned_text)
            if match:
                route_data[field] = match.group(1).strip()
            else:
                    self.logger.warning("route_data pattern not found")
        # Assign YDS and Font grades
        route_data['gradeYDS'] = gradeYDS
        route_data['gradeFont'] = gradeFont

        # Add additional data fields
        route_data['state_name'] = response.meta['state_name']
        route_data['area_id'] = response.meta['area_id']
        route_data['area_name'] = response.meta['area_name']
        route_data['route_id'] = response.meta['route_id']
        route_data['route_name'] = response.meta['route_name']

        # Append the current route data to self.route_data
        self.route_data.append(route_data)

        #### Route stats parsing from route page:
        route_id = response.meta.get('route_id')
        stat_data = {'route_id': route_id, 'avg_stars': None, 'num_votes': None}  # Initialize with default values
        # Extract stars and num votes from route stats info
        avg_stars_votes = response.xpath('//*[starts-with(@id, "starsWithAvgText-")]/text()').extract()
        for element in avg_stars_votes:
            # Extracting and cleaning the text from each matched element
            cleaned_text = ' '.join(avg_stars_votes).strip()

            # Define a regular expression pattern to match "Avg: X.X from Y votes" format
            pattern = r'Avg:\s*([\d.]+)\s*from\s*(\d+)\s*votes'

            # Use re.search to find the pattern in the text
            match = re.search(pattern, cleaned_text)

            # Check if a match was found
            if match:
                # Extract avg_stars (the first group) and convert it to a float
                avg_stars = float(match.group(1))

                # Extract num_votes (the second group) and convert it to an integer
                num_votes = int(match.group(2))

                stat_data = {
                    'route_id': route_id,
                    'avg_stars': avg_stars,
                    'num_votes': num_votes
                }
            else:
                    self.logger.warning("avg_stars, num_votes pattern not found")

        # Append the collected stat data to self.stat_data
        self.stat_data.append(stat_data)


    def closed(self, reason):
        try: 
            # Save route data as JSON
            json_route = json.dumps(self.route_data, indent=2)
            with open('route_data.json', 'w') as json_route_file:
                json_route_file.write(json_route)

            # Save area data as JSON
            json_area = json.dumps(self.area_data, indent=2)
            with open('area_data.json', 'w') as json_area_file:
                json_area_file.write(json_area)

            # Save stat data as JSON
            json_stat = json.dumps(self.stat_data, indent=2)
            with open('stat_data.json', 'w') as json_stat_file:
                json_stat_file.write(json_stat)
        except Exception as e:
            self.logger.error(f"Error while saving JSON data: {str(e)}")
        


# %%
from scrapy.crawler import CrawlerProcess
process = CrawlerProcess()
process.crawl(MtnSpider)
process.start()


