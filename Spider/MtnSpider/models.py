from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Define the base class for declarative models
Base = declarative_base()

# Define the AreaData model
class AreaData(Base):
    __tablename__ = 'area_data'
    area_id = Column(Integer, primary_key=True)
    elevation_ft = Column(String)
    GPS = Column(String)
    area_name = Column(String)
    state_name = Column(String)

# Define the RouteData model
class RouteData(Base):
    __tablename__ = 'route_data'
    route_id = Column(Integer, primary_key=True)
    climb_type = Column(String)
    climb_height_ft = Column(Float)
    climb_height_m = Column(Float)
    first_ascent = Column(String)
    page_views_total = Column(Integer)
    page_views_per_month = Column(Float)
    gradeYDS = Column(String)
    gradeFont = Column(String)
    state_name = Column(String)
    area_id = Column(Integer, ForeignKey('area_data.area_id'))
    area = relationship("AreaData")

# Define the StatData model
class StatData(Base):
    __tablename__ = 'stat_data'
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey('route_data.route_id'))
    avg_stars = Column(Float)
    num_votes = Column(Integer)
    route = relationship("RouteData")

# Function to create an SQLAlchemy engine and initialize the database
def create_sqlalchemy_engine():
    # Replace 'your_connection_string' with your actual connection string
    engine = create_engine('your_connection_string', echo=True)
    Base.metadata.create_all(engine)
    return engine

# Function to create a sessionmaker bound to the engine
def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

# Create an engine to the database
engine = create_engine('sqlite:///mtnspider_database.db')

# Create all tables defined by Base's subclasses (i.e., ExampleModel)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Remember to add new items to the session and commit them, then close the session when done.
