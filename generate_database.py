from flask import Flask
from sqlalchemy import create_engine
from declaratives.User import User
from declaratives.Dog import Dog
from declaratives.Walk import Walk
from declaratives.Walk import WalkTime

from declaratives.Base import Base

app = Flask(__name__)

app.config.from_envvar('DOGGO_TIME_SETTINGS')
engine = create_engine("postgresql://{}:{}@{}:{}/{}".format(
    app.config['DB_USER'],
    app.config['DB_PASSWORD'],
    app.config['DB_ADDRESS'],
    app.config['DB_PORT'],
    app.config['DB_NAME']
))

Base.metadata.create_all(engine)
