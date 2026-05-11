from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Tashkent")

def now_tashkent() -> datetime:
    return datetime.now(TZ)

def add_hours(dt: datetime, hours: int) -> datetime:
    return dt + timedelta(hours=hours)

def fmt(dt: datetime, fmt_str: str = "%d.%m.%Y, %H:%M") -> str:
    return dt.strftime(fmt_str)
