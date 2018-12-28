#!flask/bin/python

from flask import Flask, request, jsonify, abort, g
from flask_httpauth import HTTPBasicAuth
from passlib.hash import pbkdf2_sha256
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from declaratives.Dog import Dog
from declaratives.User import User
from declaratives.Walk import Walk, WalkTime
from validators.FieldError import FieldError
from validators.validate_add_dog import validate_add_dog
from validators.validate_add_walk import validate_add_walk
from validators.validate_register import validate_register

app = Flask(__name__)
auth = HTTPBasicAuth()

app.config.from_envvar('DOGGO_TIME_SETTINGS')
engine = create_engine("postgresql://{}:{}@{}:{}/{}".format(
    app.config['DB_USER'],
    app.config['DB_PASSWORD'],
    app.config['DB_ADDRESS'],
    app.config['DB_PORT'],
    app.config['DB_NAME']
))
Session = sessionmaker(bind=engine)


class ResponseMessage:
    SUCCESS = ''


@app.route('/api/register', methods=['POST'])
def register():
    validate_register(request)

    new_user = User(
        email=request.json['email'].lower(),
        password=pbkdf2_sha256.hash(request.json['password']),
        display_name=request.json['display_name']
    )

    session = Session()

    try:
        session.add(new_user)
        session.commit()
    except IntegrityError as e:
        if e.orig.diag.constraint_name == 'users_email_key':
            abort(400, {
                'field_errors': {
                    'email': FieldError.ALREADY_EXISTS
                }
            })

    return ResponseMessage.SUCCESS, 201


@auth.verify_password
def verify_password(email, password):
    session = Session()

    try:
        user = session.query(User).filter(User.email == email.lower()).one()
        g.user = user
        db_password = user.password
        g.session = session

    except NoResultFound:
        return False

    if not db_password:
        return False

    return pbkdf2_sha256.verify(password, db_password)


@app.route('/api')
@auth.login_required
def index():
    return ResponseMessage.SUCCESS


@app.route('/api/dog', methods=["POST"])
@auth.login_required
def add_dog():
    validate_add_dog(request)

    new_dog = Dog(name=request.json['name'])
    new_dog.users.append(g.user)
    g.session.add(new_dog)

    g.session.commit()

    return ResponseMessage.SUCCESS, 201


@app.route('/api/dog', methods=["GET"])
@auth.login_required
def dogs_list():
    return jsonify([{'id': dog.id, 'name': dog.name} for dog in g.user.dogs]), 200


@app.route('/api/walk', methods=["GET"])
@auth.login_required
def walks_list():
    walks = g.session.query(Walk).filter(Walk.dog.in_([dog.id for dog in g.user.dogs])).all()
    response = [{
        'id': walk.id,
        'date': walk.date.strftime("%Y-%m-%d"),
        'time': walk.time,
        'user': walk.user_instance.display_name,
        'dog': walk.dog_instance.name,
        'remainder': walk.remainder
    } for walk in walks]

    return jsonify(response), 200


@app.route('/api/walk', methods=["POST"])
@auth.login_required
def add_walk():
    validate_add_walk(request)

    new_walk = Walk(
        date=request.json['date'],
        user_instance=g.user,
        dog=request.json['dog'],
        time=request.json['time'],
        remainder=request.json.get('remainder')
    )

    try:
        g.session.add(new_walk)
        g.session.commit()
    except IntegrityError as e:
        if e.orig.diag.constraint_name == 'user_dog_walks_pkey':
            abort(400, {
                'error': FieldError.ALREADY_EXISTS
            })

        if e.orig.diag.constraint_name == 'user_dog_walks_dog_fkey':
            abort(400, {
                'field_errors': {
                    'dog': FieldError.INVALID
                }
            })

        if e.orig.diag.constraint_name == 'user_dog_walks_dog_fkey':
            abort(400, {
                'field_errors': {
                    'dog': FieldError.INVALID
                }
            })

        if e.orig.diag.constraint_name == 'user_dog_walks_time_fkey':
            abort(400, {
                'field_errors': {
                    'time': FieldError.INVALID
                }
            })
    except DataError:
        abort(400, {
            'field_errors': {
                'date': FieldError.INVALID
            }
        })

    return ResponseMessage.SUCCESS, 201


@app.route('/api/time', methods=["GET"])
@auth.login_required
def time_list():
    return jsonify([{
        'time': time.time,
        'time_from': time.time_from.strftime("%H:%M:%S"),
        'time_to': time.time_to.strftime("%H:%M:%S")
    } for time in g.session.query(WalkTime)]), 200


@app.errorhandler(400)
def custom400(error):
    return jsonify(error.description)


if __name__ == '__main__':
    app.run(debug=True)
