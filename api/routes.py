# api/routes.py
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Bob Ross API is running"}

@router.get("/health")
def health_check():
    return {"status": "healthy"}