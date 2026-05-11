 
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.products import Product
from app.models.category import Category
from app.schemas.products import ProductCreate
from app.schemas.category import CategoryCreate  # Endi bu xato bermaydi
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER



router = APIRouter(tags=["Admin"])

@router.post("/categories")
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_cat = Category(name=category.name)
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

@router.post("/products")   
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump()) # Pydantic v2 bo'lsa model_dump() ishlating
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


 