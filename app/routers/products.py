from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.category import Category
from typing import List

router = APIRouter(prefix="/api", tags=["Products"])

@router.get("/categories_with_products")
def get_menu(db: Session = Depends(get_db)):
    return db.query(Category).all()