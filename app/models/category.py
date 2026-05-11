# app/models/category.py
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    image_path = Column(String(255), nullable=False)  # <-- majburiy
