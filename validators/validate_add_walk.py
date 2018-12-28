from flask import abort

from validators.FieldError import FieldError


def validate_add_walk(request):
    if not request.json:
        abort(400)

    field_errors = {}

    if not request.json.get('date'):
        field_errors['date'] = FieldError.REQUIRED

    if not request.json.get('dog'):
        field_errors['dog'] = FieldError.REQUIRED

    if not request.json.get('time'):
        field_errors['time'] = FieldError.REQUIRED

    if field_errors:
        abort(400, {'field_errors': field_errors})
