# api/models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Junction tables
episode_colors = Table(
    'episode_colors', Base.metadata,
    Column('episode_id', Integer, ForeignKey('episodes.id')),
    Column('color_id', Integer, ForeignKey('colors.id'))
)

episode_subjects = Table(
    'episode_subjects', Base.metadata,
    Column('episode_id', Integer, ForeignKey('episodes.id')),
    Column('subject_id', Integer, ForeignKey('subjects.id'))
)

class Episode(Base):
    __tablename__ = 'episodes'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    air_date = Column(Date, nullable=False)
    broadcast_month = Column(Integer)
    season = Column(Integer, nullable=False)
    episode_number = Column(Integer, nullable=False)
    
    colors = relationship("Color", secondary=episode_colors, back_populates="episodes")
    subjects = relationship("Subject", secondary=episode_subjects, back_populates="episodes")

class Color(Base):
    __tablename__ = 'colors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    code = Column(String)
    
    episodes = relationship("Episode", secondary=episode_colors, back_populates="colors")

class Subject(Base):
    __tablename__ = 'subjects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    episodes = relationship("Episode", secondary=episode_subjects, back_populates="subjects")