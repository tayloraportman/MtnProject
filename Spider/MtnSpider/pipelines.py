# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from MtnSpider.items import AreaDataItems, RouteDataItems, StatDataItems  # Adjust imports as necessary
from .models import AreaData, RouteData, StatData  # Adjust the import path as needed

Base = declarative_base()


class MtnspiderPipeline:
    def __init__(self):
        self.engine = self.create_sqlalchemy_engine()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
     
    # Function to create an SQLAlchemy engine and initialize the database
    def create_sqlalchemy_engine(self):
        engine = create_engine('sqlite:///mtnspider_database.db', echo=True)
        Base.metadata.create_all(engine)
        return engine

    def process_item(self, item, spider):
        model = None
        session = self.Session()  # Create a new session for each item

        if isinstance(item, AreaDataItems):
            model = AreaData
            unique_filter = {AreaData.area_id: item['area_id']}
        elif isinstance(item, RouteDataItems):
            model = RouteData
            unique_filter = {RouteData.route_id: item['route_id']}
        elif isinstance(item, StatDataItems):
            model = StatData
            unique_filter = {StatData.route_id: item['route_id']}  # Assuming 'route_id' is a unique identifier for StatData

        if model:
            existing_record = session.query(model).filter_by(**unique_filter).first()
            if existing_record:
                # Update existing record with new information from item
                for key, value in item.items():
                    setattr(existing_record, key, value)
                spider.logger.info(f"Updated existing {model.__name__} record with ID: {unique_filter}")
            else:
                # Create a new instance of the model and add it to the session
                new_record = model(**item)
                session.add(new_record)
                spider.logger.info(f"Added new {model.__name__} record with ID: {unique_filter}")

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            spider.logger.error(f"Error processing item: {e}")
        finally:
            session.close()

        return item


    def close_spider(self, spider):
        self.session.commit()
        self.session.close()


