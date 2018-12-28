from sqlalchemy import Column, Integer, String

from .Base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    display_name = Column(String(255))
    points = Column(Integer, default=0)
