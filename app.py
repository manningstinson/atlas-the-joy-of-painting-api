import sys
sys.path.append('/workspaces/atlas-the-joy-of-painting-api/api')

from fastapi import FastAPI
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Date, create_engine
from enum import Enum
from api.routes import router
from db_connection import engine


Base = declarative_base()

class Episode(Base):
   __tablename__ = 'episodes'

   id = Column(Integer, primary_key=True)
   title = Column(String)
   air_date = Column(Date)
   broadcast_month = Column(Integer)
   season = Column(Integer)
   episode_number = Column(Integer)

class Color(Base):
   __tablename__ = 'colors'

   id = Column(Integer, primary_key=True)
   name = Column(String)
   code = Column(String)

class Subject(Base):
   __tablename__ = 'subjects'

   id = Column(Integer, primary_key=True)
   name = Column(String)

class FilterType(str, Enum):
   all = "all"
   any = "any"

app = FastAPI(title="Bob Ross API")
app.include_router(router)

# Create database tables
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)