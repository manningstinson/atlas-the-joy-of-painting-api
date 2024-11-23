import sys
sys.path.append('/workspaces/atlas-the-joy-of-painting-api/api')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Date
from enum import Enum
from api.routes import router
from db_connection import engine

# Create Base class for models
Base = declarative_base()

# Define models
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

# Initialize FastAPI app
app = FastAPI(
    title="Bob Ross API",
    description="API for The Joy of Painting data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(router)

# Create session maker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Add a health check endpoint
@app.get("/health")
async def health_check():
    try:
        # Test database connection
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}

# Don't create tables automatically in production
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)