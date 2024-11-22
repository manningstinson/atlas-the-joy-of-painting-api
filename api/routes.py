from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from .models import FilterType, Episode, Color, Subject
from sqlalchemy import text
from db_connection import get_db

router = APIRouter()

@router.get("/episodes", response_model=List[Episode])
async def get_episodes(
   db: Session = Depends(get_db),
   months: Optional[List[int]] = Query(None),
   subjects: Optional[List[str]] = Query(None),
   colors: Optional[List[str]] = Query(None),
   filter_type: FilterType = FilterType.all
):
   try:
       query = """
       WITH filtered_episodes AS (
           SELECT DISTINCT e.id, e.title, e.air_date, e.broadcast_month, e.season, e.episode_number
           FROM episodes e
           LEFT JOIN episode_subjects es ON e.id = es.episode_id
           LEFT JOIN subjects s ON es.subject_id = s.id
           LEFT JOIN episode_colors ec ON e.id = ec.episode_id
           LEFT JOIN colors c ON ec.color_id = c.id
           WHERE 1=1
       """
       params = {}
       conditions = []

       if months:
           conditions.append("broadcast_month = ANY(:months)")
           params['months'] = months

       if subjects:
           conditions.append("LOWER(s.name) = ANY(:subjects)")
           params['subjects'] = [s.lower() for s in subjects]

       if colors:
           conditions.append("LOWER(c.name) = ANY(:colors)")
           params['colors'] = [c.lower() for c in colors]

       if conditions:
           if filter_type == FilterType.all:
               for i, condition in enumerate(conditions):
                   query += f" AND EXISTS (SELECT 1 FROM episodes e2 WHERE e2.id = e.id AND {condition})"
           else:
               query += " AND (" + " OR ".join(conditions) + ")"

       query += ")"
       query += """
           SELECT DISTINCT * FROM filtered_episodes
           ORDER BY air_date;
       """

       result = db.execute(text(query), params)
       rows = result.mappings().all()
       return [Episode(**dict(row)) for row in rows]

   except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))

@router.get("/colors", response_model=List[Color])
async def get_colors(db: Session = Depends(get_db)):
   try:
       result = db.execute(text("SELECT id, name, code FROM colors ORDER BY name"))
       rows = result.mappings().all()
       return [Color(**dict(row)) for row in rows]
   except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))

@router.get("/subjects", response_model=List[Subject])
async def get_subjects(db: Session = Depends(get_db)):
   try:
       result = db.execute(text("SELECT id, name FROM subjects ORDER BY name"))
       rows = result.mappings().all()
       return [Subject(**dict(row)) for row in rows]
   except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))