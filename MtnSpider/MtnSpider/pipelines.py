# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
from scrapy.exceptions import DropItem
import json
from MtnSpider.items import AreaData, RouteData, StatData


# Revised version of MtnspiderPipeline to handle multiple JSON structures

class MtnspiderPipeline:
    # Initialize the pipeline
    def __init__(self):
        self.create_connection()
        self.create_table()

    # Create a SQLite connection
    def create_connection(self):
        self.conn = sqlite3.connect('mtnspider_json.db')
        self.curr = self.conn.cursor()

    # Create tables for storing different JSON data types
    def create_table(self):
        # Adjust these table creation queries based on your actual data structures
        self.curr.execute("""DROP TABLE IF EXISTS area_data""")
        self.curr.execute("""create table area_data(data text)""")

        self.curr.execute("""DROP TABLE IF EXISTS route_data""")
        self.curr.execute("""create table route_data(data text)""")

        self.curr.execute("""DROP TABLE IF EXISTS stat_data""")
        self.curr.execute("""create table stat_data(data text)""")

    # Process each item
    def process_item(self, item, spider):
        # Convert item to a dictionary
        item_dict = dict(item)  # or use ItemAdapter(item).asdict() if scrapy.ItemAdapter is available

        # Serialize item to JSON
        json_data = json.dumps(item_dict)

        # Determine the type of item and store accordingly
        if isinstance(item, AreaData):
            self.store_db(json_data, 'area_data')
        elif isinstance(item, RouteData):
            self.store_db(json_data, 'route_data')
        elif isinstance(item, StatData):
            self.store_db(json_data, 'stat_data')
        return item

    # Store item as JSON in the appropriate table
    def store_db(self, item, table_name):
        self.curr.execute(f"insert into {table_name} values (?)", 
                          (json.dumps(item),))
        self.conn.commit()

    # Close the database connection
    def close_spider(self, spider):
        self.conn.close()

# Note: In your actual implementation, you will need to define AreaData, RouteData, and StatData, or adjust the logic to match your item types.
# Also, ensure to adjust the table creation queries and data processing as per your data structure.
