 
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.products import Product
from app.models.marking import Marking

async def create_marking(db: Session, product_id: int, user_id: int) -> Marking:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    now = datetime.now()
    expires = now + timedelta(days=int(product.storage_days or 0))

    m = Marking(
        product_id=product.id,
        user_id=user_id,
        created_at=now,
        expires_at=expires
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m
