import scrapy
import pandas as pd
import logging
import re
from urllib.parse import urlparse
from ..items import AreaDataItems, RouteDataItems, StatDataItems
from .mtn_proj_spider import MtnSpider 



class MtnSpiderTest(MtnSpider):
    name = 'mtnspidertest'
    # Replace the start URL with a direct route URL
    start_urls = ['https://www.mountainproject.com/route/105732422/epinephrine']
 


    def parse(self, response):
        response.meta.update({
            'state_name': 'Dummy Area',
            'area_id': '12345',
            'area_name': 'Dummy Area',
            'route_id': '67890',
            'route_name': 'Dummy Route'
        })
        return self.parse_routes(response)

    def parse_stat(self, response):
         response.meta.update({
            'route_id': '67890',   
        })
         return self.extract_route_stats(response)
