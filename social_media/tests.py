from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from authentication.models import User


class BaseAPITest(APITestCase):

    def create(self, email='test@mail.com', first_name='John', last_name='Doe', password='test_password'):
        user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name, password=password)
        user.last_login = timezone.now()
        user.is_active = True
        user.save()

        return user

    def create_and_login(self, email='test@mail.com', first_name='John', last_name='Doe', password='test_password'):
        user = self.create(email=email, first_name=first_name, last_name=last_name, password=password)
        self.authorize(user)
        return user

    def authorize(self, user, **additional_headers):
        token = AccessToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"{api_settings.AUTH_HEADER_TYPES[0]} {token}",
            **additional_headers
        )

    def logout(self, **additional_headers):
        self.client.credentials(**additional_headers)
