from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authentication.validators import ValidateEmailSerializerMixin
from authentication.models import User


class SignUpSerializer(ValidateEmailSerializerMixin, serializers.ModelSerializer):
    """Serializer for creating user objects."""

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "password")
        read_only_fields = ("id",)

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """We use CustomTokenObtainPairSerializer which inherited from TokenObtainPairSerializer,
    for custom error message.
    """
    default_error_messages = {
        'no_active_account': 'Entered email address or password incorrect. Please, try again.'
    }


class CurrentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")
        read_only_fields = ("id",)
