from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from .Base import Base


class Dog(Base):
    __tablename__ = 'dogs'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255))

    users = relationship(
        "User",
        secondary=Table('users_dogs', Base.metadata,
                        Column("user", Integer, ForeignKey('users.id'),
                               primary_key=True),
                        Column("dog", Integer, ForeignKey('dogs.id'),
                               primary_key=True)
                        ),
        backref="dogs"
    )
