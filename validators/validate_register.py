import re

from flask import abort
from validate_email import validate_email

from .FieldError import FieldError

password_pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'


def validate_register(request):
    if not request.json:
        abort(400)

    field_errors = {}

    if not request.json.get('email'):
        field_errors['email'] = FieldError.REQUIRED
    elif not validate_email(request.json['email']):
        field_errors['email'] = FieldError.INVALID

    if not request.json.get('password'):
        field_errors['password'] = FieldError.REQUIRED
    elif re.match(password_pattern, request.json['password']):
        field_errors['password'] = FieldError.INVALID

    if not request.json.get('display_name'):
        field_errors['display_name'] = FieldError.REQUIRED

    if field_errors:
        abort(400, {'field_errors': field_errors})
