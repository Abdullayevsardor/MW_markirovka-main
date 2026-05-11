# # app/routers/admin_ui.py
# from __future__ import annotations

# from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, HTTPException
# from fastapi.responses import RedirectResponse
# from starlette.status import HTTP_303_SEE_OTHER
# from sqlalchemy.orm import Session
# from pathlib import Path
# from uuid import uuid4
# import shutil

# from app.db.session import get_db
# from app.models.category import Category
# from app.models.products import Product

# router = APIRouter(tags=["UI"])

# # ---------------------------
# # CONFIG
# # ---------------------------
# BRAND_NAME = "MAXWAY"
# ADMIN_TOKEN = "ok"          # oddiy token (keyin JWT qilamiz)

# BASE_DIR = Path(__file__).resolve().parent.parent.parent  # project root
# STATIC_DIR = BASE_DIR / "static"
# CATEGORY_DIR = STATIC_DIR / "category"
# CATEGORY_DIR.mkdir(parents=True, exist_ok=True)


# def _require_admin(request: Request) -> None:
#     token = request.query_params.get("token")
#     if token != ADMIN_TOKEN:
#         raise HTTPException(status_code=401, detail="Not authorized")


# def _save_category_image(file: UploadFile) -> str:
#     # ext aniqlash (oddiy)
#     ext = ".png"
#     if file.filename and "." in file.filename:
#         ext0 = "." + file.filename.rsplit(".", 1)[1].lower()
#         if ext0 in [".png", ".jpg", ".jpeg", ".webp"]:
#             ext = ext0

#     filename = f"{uuid4().hex}{ext}"
#     save_path = CATEGORY_DIR / filename

#     with save_path.open("wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     # web url (template shu bilan ochadi)
#     return f"/static/category/{filename}"


# # ---------------------------
# # USER UI (DEFAULT PAGE)
# # ---------------------------
# @router.get("/")
# def user_home(request: Request, db: Session = Depends(get_db)):
#     categories = db.query(Category).order_by(Category.name.asc()).all()
#     return request.app.state.templates.TemplateResponse(
#         "user.html",
#         {"request": request, "categories": categories, "brand_name": BRAND_NAME}
#     )


# @router.get("/category/{category_id}")
# def user_category(request: Request, category_id: int, db: Session = Depends(get_db)):
#     category = db.query(Category).filter(Category.id == category_id).first()
#     if not category:
#         raise HTTPException(status_code=404, detail="Category not found")

#     products = db.query(Product).filter(Product.category_id == category_id).order_by(Product.name.asc()).all()
#     return request.app.state.templates.TemplateResponse(
#         "category.html",
#         {
#             "request": request,
#             "category": category,
#             "products": products,
#             "brand_name": BRAND_NAME
#         }
#     )


# # ---------------------------
# # ADMIN LOGIN
# # ---------------------------
# @router.get("/admin-login")
# def admin_login_page(request: Request):
#     return request.app.state.templates.TemplateResponse(
#         "admin_login.html",
#         {"request": request, "brand_name": BRAND_NAME}
#     )


# @router.post("/admin-login")
# def admin_login(password: str = Form(...)):
#     if password != ADMIN_PASSWORD:
#         return RedirectResponse("/admin-login?err=bad_password", status_code=HTTP_303_SEE_OTHER)
#     return RedirectResponse(f"/admin?token={ADMIN_TOKEN}", status_code=HTTP_303_SEE_OTHER)


# # ---------------------------
# # ADMIN PANEL
# # ---------------------------
# @router.get("/admin")
# def admin_page(request: Request, db: Session = Depends(get_db)):
#     _require_admin(request)

#     categories = db.query(Category).order_by(Category.name.asc()).all()
#     products = db.query(Product).order_by(Product.id.desc()).all()

#     return request.app.state.templates.TemplateResponse(
#         "admin.html",
#         {
#             "request": request,
#             "categories": categories,
#             "products": products,
#             "brand_name": BRAND_NAME,
#             "token": request.query_params.get("token"),
#         }
#     )


# @router.post("/admin/category")
# async def admin_create_category(
#     request: Request,
#     name: str = Form(...),
#     category_image: UploadFile = File(...),   # ✅ majburiy
#     db: Session = Depends(get_db),
# ):
#     _require_admin(request)

#     name = name.strip()
#     if not name:
#         return RedirectResponse(f"/admin?token={ADMIN_TOKEN}&err=category_empty", status_code=HTTP_303_SEE_OTHER)

#     exists = db.query(Category).filter(Category.name == name).first()
#     if exists:
#         return RedirectResponse(f"/admin?token={ADMIN_TOKEN}&err=category_exists", status_code=HTTP_303_SEE_OTHER)

#     if not category_image or not category_image.filename:
#         return RedirectResponse(f"/admin?token={ADMIN_TOKEN}&err=category_image_required", status_code=HTTP_303_SEE_OTHER)

#     image_path = _save_category_image(category_image)

#     db_cat = Category(name=name, image_path=image_path)
#     db.add(db_cat)
#     db.commit()

#     return RedirectResponse(f"/admin?token={ADMIN_TOKEN}&ok=category_created", status_code=HTTP_303_SEE_OTHER)


# @router.post("/admin/product")
# def admin_create_product(
#     request: Request,
#     name: str = Form(...),
#     category_id: int = Form(...),
#     storage_days: int = Form(...),
#     temp_range: str = Form(...),
#     storage_temp: str = Form(...),
#     shelf_life_hours: int = Form(...),
#     db: Session = Depends(get_db),
# ):
#     _require_admin(request)

#     name = name.strip()
#     temp_range = temp_range.strip()
#     storage_temp = storage_temp.strip()

#     if not name:
#         return RedirectResponse(f"/admin?token={ADMIN_TOKEN}&err=product_empty", status_code=HTTP_303_SEE_OTHER)

#     # Shelf-life avtomatik: kun * 24
#     if storage_days and (not shelf_life_hours or shelf_life_hours <= 0):
#         shelf_life_hours = storage_days * 24

#     product = Product(
#         name=name,
#         category_id=category_id,
#         storage_days=storage_days,
#         temp_range=temp_range,
#         storage_temp=storage_temp,
#         shelf_life_hours=shelf_life_hours,
#         # image_path productda majburiy emas (xohlasangiz keyin qo‘shamiz)
#     )
#     db.add(product)
#     db.commit()

#     return RedirectResponse(f"/admin?token={ADMIN_TOKEN}&ok=product_created", status_code=HTTP_303_SEE_OTHER)
