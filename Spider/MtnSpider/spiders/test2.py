import scrapy
import pandas as pd
import logging
import re
from urllib.parse import urlparse
from ..items import AreaDataItems, RouteDataItems, StatDataItems
from .mtn_proj_spider import MtnSpider 

class MtnSpiderTest(MtnSpider):
    name = 'mtnspidertest2'
    start_urls = ['https://www.mountainproject.com/route/105732422/epinephrine']

    def parse(self, response):
        # Pre-set metadata for testing
        response.meta.update({
            'state_name': 'Dummy Area',
            'area_id': '12345',
            'area_name': 'Dummy Area',
            'route_id': '67890',
            'route_name': 'Dummy Route'
        })
        return self.parse_routes(response)

    def parse_routes(self, response):
        # Assuming parse_routes yields RouteDataItems, capture and print it
        route_item = super().parse_routes(response)
        print("Route Data Extracted:")
        print(route_item)  # This assumes route_item is a dictionary-like object
        yield route_item

    def extract_route_stats(self, response):
        # Update response.meta for stat data extraction
        response.meta.update({'route_id': '67890'})
        stat_item = super().extract_route_stats(response)
        print("Stat Data Extracted:")
        print(stat_item)  # Assuming stat_item is a dictionary-like object
        yield stat_item