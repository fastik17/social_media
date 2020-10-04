from rest_framework.exceptions import ValidationError

from authentication.models import User


class ValidateEmailSerializerMixin:

    def validate_email(self, value):
        """Convert email to lower case and check if email already exists"""
        value = value.lower()
        if User.objects.filter(email=value).exists():
            raise ValidationError('User with this email address already exists.')
        return value
