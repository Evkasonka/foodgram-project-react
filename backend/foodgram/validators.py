import re

from django.core.exceptions import ValidationError
from foodgram.errors import ErrorMesage

REGEX_FOR_USERNAME = re.compile(r"^[\w.@+-]+")


def validate_username(name):
    if not REGEX_FOR_USERNAME.fullmatch(name):
        raise ValidationError(ErrorMesage.ALLOWED_NAME)
