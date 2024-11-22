from fastapi import FastAPI
from .routes import router
from db_connection import Base, engine  # Update this line

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bob Ross API")
app.include_router(router)