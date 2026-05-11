 
from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    # storage_days: int
    temp_range: str
    category_id: int
    # Bu maydonlarni ham qo'shing:
    storage_temp: Optional[str] = None
    shelf_life_hours: Optional[int] = None
    image_path: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True