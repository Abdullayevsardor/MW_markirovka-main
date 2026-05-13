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
print("STATIC_DIR:", STATIC_DIR)
print("FILES:", os.listdir(STATIC_DIR))
print("CATEGORY:", os.listdir(os.path.join(STATIC_DIR, "category")))

# Routers
app.include_router(ui.router)
app.include_router(marking.router, prefix="/api/marking", tags=["Marking"])

# DEBUG handler
@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    print(tb) # Konsolda xatoni to'liq ko'rish uchun
    return PlainTextResponse(f"Internal Server Error:\n{tb}", status_code=500)
