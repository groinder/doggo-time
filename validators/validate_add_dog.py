from flask import abort

from validators.FieldError import FieldError


def validate_add_dog(request):
    if not request.json:
        abort(400)

    field_errors = {}

    if not request.json.get('name'):
        field_errors['name'] = FieldError.REQUIRED

    if field_errors:
        abort(400, {'field_errors': field_errors})
