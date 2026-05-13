from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import traceback
from fastapi.responses import PlainTextResponse

from app.routers import marking, ui
from app.config import settings
# 1. Bazani va modellarni import qiling

from app.db.session import engine, Base
from app.db import base # Modellaringiz yig'ilgan Base klasini import qiling
import os
import shutil


BASE_DIR = Path(__file__).resolve().parent


# Jadvallarni yaratish (bu xatolikni yo'qotadi)
Base.metadata.create_all(bind=engine)

# 2. Jadvallarni avtomatik yaratish (Alembic ishlatilmagan bo'lsa)
# Bu kod app obyektidan oldin yoki startup eventda bo'lishi kerak

app = FastAPI(
    title="Maxway Marking System",
    # docs_url="/docs",
    docs_url=None,
    redoc_url=None
)



STATIC_DIR = os.path.join(os.getcwd(), "static")   # /app/static
os.makedirs(os.path.join(STATIC_DIR, "category"), exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory="app/templates")
app.state.templates = templates
 

STATIC_CATEGORY = "/app/static/category"
SOURCE_CATEGORY = "/app/source_images"

os.makedirs(STATIC_CATEGORY, exist_ok=True)

print("STATIC BEFORE:", os.listdir(STATIC_CATEGORY))

# agar volume bo'sh bo'lsa
if len(os.listdir(STATIC_CATEGORY)) <= 1:
    if os.path.exists(SOURCE_CATEGORY):

        for file in os.listdir(SOURCE_CATEGORY):
            src = os.path.join(SOURCE_CATEGORY, file)
            dst = os.path.join(STATIC_CATEGORY, file)

            if os.path.isfile(src):
                shutil.copy2(src, dst)

print("STATIC AFTER:", os.listdir(STATIC_CATEGORY))



# Routers
app.include_router(ui.router)
app.include_router(marking.router, prefix="/api/marking", tags=["Marking"])

# DEBUG handler
@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    print(tb) # Konsolda xatoni to'liq ko'rish uchun
    return PlainTextResponse(f"Internal Server Error:\n{tb}", status_code=500)
