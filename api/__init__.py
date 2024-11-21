# api/__init__.py
from fastapi import FastAPI
from .routes import router
from . import models
from .utils import engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bob Ross API")
app.include_router(router)