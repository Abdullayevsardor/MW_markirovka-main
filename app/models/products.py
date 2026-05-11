# app/models/product.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    # storage_days = Column(Integer)
    temp_range = Column(String)
    # Mana bu ikki qatorni qo'shing:
    storage_temp = Column(String, nullable=True) 
    shelf_life_hours = Column(Integer, nullable=True)
    
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category")
    image_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
