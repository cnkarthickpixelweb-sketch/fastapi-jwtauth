from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME,DB

if DB == 'psql':
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


if DB == 'mysql':
    DATABASE_URL = (
        f"mysql+pymysql://{DB_USER}@{DB_HOST}/{DB_NAME}"
    )

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()