from sqlalchemy import Column,Integer,String
from app.db.database import Base


## USERS TABLE
class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    profile_image = Column(String, nullable=True)