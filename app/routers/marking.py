from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.products import Product
from fastapi.templating import Jinja2Templates

from app.utils.time import now_tashkent, add_hours, fmt  

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/print/{product_id}")
def print_sticker(product_id: int, request: Request, marker_name: str = Query("Noma'lum"), db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Mahsulot topilmadi")

    try:
        hours = int(product.shelf_life_hours or 0)
    except (ValueError, TypeError):
        hours = 0

    created_dt = now_tashkent()
    expires_dt = add_hours(created_dt, hours)

    temp = str(product.temp_range)
    if ".." in temp or "-" in temp:
        display_temp = temp
    elif temp.isdigit():
        display_temp = f"{temp}+"
    else:
        display_temp = temp

    return templates(request).TemplateResponse(
        "sticker.html",
        {
            "request": request,
            "product": product,
            "display_temp": display_temp,
            "storage_hours": hours,
            "created_at": fmt(created_dt),
            "expires_at": fmt(expires_dt),
            "username": marker_name,
            "brand": "Maxway",
        }
    )
