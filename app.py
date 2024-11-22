import sys
import os
sys.path.append('/workspaces/atlas-the-joy-of-painting-api/api')

from flask import Flask, jsonify, request
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Date
from enum import Enum
from api.routes import get_episodes, get_colors, get_subjects
from api.utils import get_db

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

app = Flask(__name__)

app.route('/episodes', methods=['GET'])(get_episodes)
app.route('/colors', methods=['GET'])(get_colors)
app.route('/subjects', methods=['GET'])(get_subjects)

@app.route('/episodes', methods=['GET'])
def get_episodes():
    filter_type = request.args.get('filter_type', FilterType.all)
    months = request.args.getlist('months', type=int)
    subjects = request.args.getlist('subjects')
    colors = request.args.getlist('colors')

    episodes = get_episodes(filter_type, months, subjects, colors)
    return jsonify([e.as_dict() for e in episodes])

@app.route('/colors', methods=['GET'])
def get_colors():
    colors = get_colors()
    return jsonify([c.as_dict() for c in colors])

@app.route('/subjects', methods=['GET'])
def get_subjects():
    subjects = get_subjects()
    return jsonify([s.as_dict() for s in subjects])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))