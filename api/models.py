# models.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from enum import Enum

class FilterType(str, Enum):
    all = "all"
    any = "any"

class Episode(BaseModel):
    id: int
    title: str
    air_date: date
    broadcast_month: int
    season: int
    episode_number: int

class Color(BaseModel):
    id: int
    name: str
    code: Optional[str]

class Subject(BaseModel):
    id: int
    name: str

class FilterParams(BaseModel):
    months: Optional[List[int]] = None
    subjects: Optional[List[str]] = None
    colors: Optional[List[str]] = None
    filter_type: FilterType = FilterType.all