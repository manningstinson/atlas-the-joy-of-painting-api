# api/__init__.py
from fastapi import FastAPI

app = FastAPI()

# Import your routes
from .routes import router
app.include_router(router)