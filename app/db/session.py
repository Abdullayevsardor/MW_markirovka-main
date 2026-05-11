from email.mime import base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from sqlalchemy.orm import declarative_base



SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:1234@db:5432/marking_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)



SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
