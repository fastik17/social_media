from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.reverse import reverse

from authentication.models import User
from social_media.tests import BaseAPITest


class TestCreateSuperuser(BaseAPITest):

    def test_create_superuser(self):
        first_name = "John"
        last_name = "Doe"
        user = User.objects.create_superuser("admin@mail.com", first_name, last_name, "test_password")
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class TestObtainJSONWebTokenView(BaseAPITest):

    def setUp(self):
        self.email = "test@mail.com"
        self.password = "test_password"
        self.user = self.create(email=self.email, password=self.password)

    def test_get_token_pair(self):
        resp = self.client.post(reverse('v1:auth:auth'), data={'email': self.email, 'password': self.password})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('refresh', resp.data)
        self.assertIn('access', resp.data)

    def test_get_token_authentication_error(self):
        resp = self.client.post(reverse('v1:auth:auth'), data={'email': 'fake_data', 'password': 'fake_data'})
        self.assertEqual(resp.status_code, 401)


class TestVerifyJSONWebTokenView(BaseAPITest):

    def setUp(self):
        self.email = "test@mail.com"
        self.password = "test_password"
        self.user = self.create(email=self.email, password=self.password)
        self.access_token = str(AccessToken.for_user(self.user))

    def test_token_is_valid(self):
        resp = self.client.post(reverse('v1:auth:auth-verify'), data={'token': self.access_token})
        self.assertEqual(resp.status_code, 200)

    def test_get_token_validation_error(self):
        resp = self.client.post(reverse('v1:auth:auth-verify'), data={'token': 'fake_data'})
        self.assertEqual(resp.status_code, 401)


class TestRefreshJSONWebTokenView(BaseAPITest):

    def setUp(self):
        self.email = "test@mail.com"
        self.password = "test_password"
        self.user = self.create(email=self.email, password=self.password)
        self.refresh_token = str(RefreshToken.for_user(self.user))

    def test_get_access_token(self):
        resp = self.client.post(reverse('v1:auth:auth-refresh'), data={'refresh': self.refresh_token})
        self.assertIn('access', resp.data)

    def test_get_token_refresh_error(self):
        resp = self.client.post(reverse('v1:auth:auth-refresh'), data={'refresh': 'fake_data'})
        self.assertEqual(resp.status_code, 401)


class TestSignUpView(BaseAPITest):

    def setUp(self):
        self.required_data = {
            "first_name": "John",
            "email": "test@test.com",
            "last_name": "Doe",
            "password": "hello1234567!"
        }

    def test_sign_up_required(self):
        resp = self.client.post(reverse('v1:auth:sign-up'), data=self.required_data)
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(User.objects.filter(
            first_name=self.required_data['first_name'],
            email=self.required_data['email'],
            last_name=self.required_data['last_name'],
        ).exists())

    def test_sign_up_email_to_lower_case(self):
        self.required_data['email'] = 'NEw_mail@mail.com'
        resp = self.client.post(reverse('v1:auth:sign-up'), data=self.required_data)
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(User.objects.filter(
            first_name=self.required_data['first_name'],
            email=self.required_data['email'].lower(),
            last_name=self.required_data['last_name'],
        ).exists())

    def test_sign_up_user_exists(self):
        email = 'test@test.com'
        self.create(email=email)
        self.required_data['email'] = email
        resp = self.client.post(reverse('v1:auth:sign-up'), data=self.required_data)
        self.assertEqual(resp.status_code, 400)


