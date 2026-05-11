from fastapi import APIRouter, Depends, Request, Form, UploadFile, File
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from sqlalchemy.orm import Session
import os, uuid

from app.db.session import get_db
from app.models.category import Category
from app.models.products import Product
# from app.config import ADMIN_PASSWORD
from app.config import settings

router = APIRouter(tags=["UI"])

def get_templates(request: Request):
    return request.app.state.templates

# -------------------------
# USER: Default page "/"
# -------------------------
@router.get("/")
def user_home(request: Request, db: Session = Depends(get_db)):
    cats = db.query(Category).order_by(Category.id.asc()).all()
    return templates(request).TemplateResponse(
        "user_home.html",
        {"request": request, "brand": "MAXWAY", "categories": cats}
    )

# USER: Category products
@router.get("/category/{category_id}")
def user_category(request: Request, category_id: int, db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.id == category_id).first()
    # products = db.query(Product).filter(Product.category_id == category_id).order_by(Product.id.desc()).all()
    products = (
        db.query(Product)
        .filter(Product.category_id == category_id)
        .order_by(Product.id.asc())
        .all()
    )

    return templates(request).TemplateResponse(
        # "index.html",
        "category_products.html",
        {"request": request, "brand": "MAXWAY", "category": cat, "products": products}
    )

# USER: Admin button -> password page
@router.get("/admin-login")
def admin_login_page(request: Request):
    return templates(request).TemplateResponse(
        "admin_login.html",
        {"request": request, "brand": "MAXWAY"}
    )

@router.post("/admin-login")
def admin_login(password: str = Form(...)):
    if password != settings.ADMIN_PASSWORD:
        return RedirectResponse(url="/admin-login?err=1", status_code=HTTP_303_SEE_OTHER)
    # oddiy variant: query param bilan
    return RedirectResponse(url="/admin?token=ok", status_code=HTTP_303_SEE_OTHER)


@router.post("/admin/category/delete")
def admin_delete_category(
    request: Request,
    token: str | None = None,
    category_id: int = Form(...),
    db: Session = Depends(get_db),
):
    if token != "ok":
        return RedirectResponse(url="/admin-login", status_code=HTTP_303_SEE_OTHER)

    # 1) Avval shu categoryga tegishli productlar bor-yo'qligini tekshiramiz
    prod_count = db.query(Product).filter(Product.category_id == category_id).count()

    # Variant A (oddiy user uchun qulay): productlar ham bo'lsa o'chirib yuboramiz
    if prod_count > 0:
        db.query(Product).filter(Product.category_id == category_id).delete(synchronize_session=False)

    if not category_id:
        return RedirectResponse(url="/admin?token=ok&err=category_select_required", status_code=HTTP_303_SEE_OTHER)

    # 2) Categoryni o'chiramiz
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        return RedirectResponse(url="/admin?token=ok&err=category_not_found", status_code=HTTP_303_SEE_OTHER)
    
   

    db.delete(cat)
    db.commit()

    return RedirectResponse(url="/admin?token=ok&ok=category_deleted", status_code=HTTP_303_SEE_OTHER)

@router.get("/admin")
def admin_page(request: Request, token: str | None = None, db: Session = Depends(get_db)):
    if token != "ok":
        return RedirectResponse(url="/admin-login", status_code=HTTP_303_SEE_OTHER)

    cats = db.query(Category).order_by(Category.id.asc()).all()
    products = db.query(Product).order_by(Product.id.desc()).all()

    return templates(request).TemplateResponse(
        "admin.html",
        {
            "request": request,
            "brand": "MAXWAY",
            "categories": cats,
            "products": products
        }
    )

# ADMIN: Create category (image REQUIRED)
# @router.post("/admin/category")
# def admin_create_category(
#     token: str = Form(...),
#     name: str = Form(...),
#     category_image: UploadFile = File(...),
#     db: Session = Depends(get_db),
# ):
#     if token != "ok":
#         return RedirectResponse(url="/admin-login", status_code=HTTP_303_SEE_OTHER)

#     name = name.strip()
#     if not name:
#         return RedirectResponse(url="/admin?token=ok&err=category_empty", status_code=HTTP_303_SEE_OTHER)

#     exists = db.query(Category).filter(Category.name == name).first()
#     if exists:
#         return RedirectResponse(url="/admin?token=ok&err=category_exists", status_code=HTTP_303_SEE_OTHER)

#     os.makedirs("static/category", exist_ok=True)
#     ext = os.path.splitext(category_image.filename or "")[1].lower() or ".jpg"
#     filename = f"{uuid.uuid4().hex}{ext}"
#     save_path = os.path.join("static", "category", filename)

#     with open(save_path, "wb") as f:
#         f.write(category_image.file.read())

#     cat = Category(name=name, image_path="/" + save_path.replace("\\", "/"))
#     db.add(cat)
#     db.commit()

#     return RedirectResponse(url="/admin?token=ok&ok=category_created", status_code=HTTP_303_SEE_OTHER)



import shutil # Qo'shildi

@router.post("/admin/category")
def admin_create_category(
    token: str = Form(...),
    name: str = Form(...),
    category_image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if token != "ok":
        return RedirectResponse(url="/admin-login", status_code=HTTP_303_SEE_OTHER)

    name = name.strip()
    if not name:
        return RedirectResponse(url="/admin?token=ok&err=category_empty", status_code=HTTP_303_SEE_OTHER)

    # Papka mavjudligini tekshirish (Railway Volume uchun)
    upload_dir = os.path.join("static", "category")
    os.makedirs(upload_dir, exist_ok=True)

    # Fayl nomini yaratish
    ext = os.path.splitext(category_image.filename or "")[1].lower() or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(upload_dir, filename)

    # Rasmni saqlash (shutil bilan xavfsizroq)
    try:
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(category_image.file, buffer)
    finally:
        category_image.file.close()

    # BAZA UCHUN YO'L: Aniq qilib yozamiz
    db_path = f"static/category/{filename}"

    cat = Category(name=name, image_path=db_path)
    db.add(cat)
    db.commit()

    return RedirectResponse(url="/admin?token=ok&ok=category_created", status_code=HTTP_303_SEE_OTHER)

# ADMIN: Create product
@router.post("/admin/product")
def admin_create_product(
    token: str = Form(...),
    category_id: int = Form(...),
    name: str = Form(...),
    # storage_days: int = Form(...),
    shelf_life_hours: int = Form(...),
    temp_range: str = Form(...),
    storage_temp: str = Form(...),
    db: Session = Depends(get_db),
):
    if token != "ok":
        return RedirectResponse(url="/admin-login", status_code=HTTP_303_SEE_OTHER)

    p = Product(
        category_id=category_id,
        name=name.strip(),
        # storage_days=storage_days,
        shelf_life_hours=shelf_life_hours,
        temp_range=temp_range.strip(),
        storage_temp=storage_temp.strip(),
    )
    db.add(p)
    db.commit()
    return RedirectResponse(url="/admin?token=ok&ok=product_created", status_code=HTTP_303_SEE_OTHER)


@router.post("/admin/product/delete/{product_id}")
def delete_product(product_id: int, request: Request, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return {"error": "Товар не найден"}
    db.delete(product)
    db.commit()
    return {"ok": True}
