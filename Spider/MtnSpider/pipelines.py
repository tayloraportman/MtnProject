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
        session = self.Session()
        unique_key = None

        # Determine the model and construct unique_filter with string keys
        if isinstance(item, AreaDataItems):
            model = AreaData
            unique_key = 'area_id'
        elif isinstance(item, RouteDataItems):
            model = RouteData
            unique_key = 'route_id'
        elif isinstance(item, StatDataItems):
            model = StatData
            unique_key = 'route_id'

        # Ensure unique_key exists in the item
        if model and unique_key and unique_key in item:
            unique_filter = {unique_key: item[unique_key]}
            existing_record = session.query(model).filter_by(**unique_filter).first()

            if existing_record:
                # Update existing record with item fields that match the model's columns
                for key in model.__table__.columns.keys():
                    if key in item:
                        setattr(existing_record, key, item[key])
                spider.logger.info(f"Updated existing {model.__name__} record with ID: {unique_filter}")
            else:
                # Filter item fields to match model's columns and create a new record
                item_fields = {k: item[k] for k in item if k in model.__table__.columns.keys()}
                new_record = model(**item_fields)
                session.add(new_record)
                spider.logger.info(f"Added new {model.__name__} record with ID: {unique_filter}")
        else:
            if unique_key is None:
                spider.logger.warning("Received an item that doesn't match expected models.")
            else:
                spider.logger.warning(f"Item does not contain expected key '{unique_key}'.")

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


