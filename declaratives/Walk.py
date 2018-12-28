from sqlalchemy import Column, Integer, Date, ForeignKey, String, Time
from sqlalchemy.orm import relationship


from declaratives.Base import Base


class WalkTime(Base):
    __tablename__ = 'walk_time'

    time = Column(String(255), primary_key=True, unique=True)
    time_from = Column(Time)
    time_to = Column(Time)


class Walk(Base):
    __tablename__ = 'user_dog_walks'

    id = Column(Integer, unique=True, autoincrement=True)
    date = Column(Date,  primary_key=True)
    user = Column(Integer, ForeignKey('users.id'),  primary_key=True)
    dog = Column(Integer, ForeignKey('dogs.id'),  primary_key=True)
    time = Column(String(255), ForeignKey('walk_time.time'),  primary_key=True)
    remainder = Column(Date, nullable=True)

    walk_time = relationship('WalkTime')
    dog_instance = relationship('Dog')
    user_instance = relationship('User')
