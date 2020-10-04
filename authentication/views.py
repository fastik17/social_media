from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenVerifySerializer, TokenRefreshSerializer


from authentication.serializers import SignUpSerializer, CustomTokenObtainPairSerializer


class ObtainJSONWebToken(TokenObtainPairView):
    """
    post:
    Generate REST API token.

    Generate personal REST API token with expired date `ACCESS_TOKEN_LIFETIME_HOURS` or/and
    `ACCESS_TOKEN_LIFETIME_MINUTES` (1 day).

    In a few words - it's an authentication token. To work with API you need to have it, entering your email
    and password. Each time you request to the API, you need to send in header your token like
    `Authorization: JWT eyJ0eXAiOiJKV...`, where `JWT` is header authorization prefix.

    ### Examples

    If data is successfully processed the server returns status code `200`.

    ```json
    {
        "email": "kyiv@example.com",
        "password": "nihao123"
    }
    ```

    ### Errors

    If there were some error in client data, it sends status code `401`.
    """
    serializer_class = CustomTokenObtainPairSerializer


class VerifyJSONWebToken(TokenVerifyView):
    """
    post:
    Verify your token (is it valid?)

    To work with API you need to have valid (verified) token which you get after visiting `/auth/token-verify`
    url, entering your token.[Read JWT docs](https://jwt.io/)

    ### Examples

    If data is successfully processed the server returns status code `200`.

    ```json
    {
        "token": "7wq3vkdlgnkngdDFHGergergEGRerRGEgerEReerE346346vergd456456"
    }
    ```

    ### Errors

    If there were some error in client data, it sends status code `401` with the error message looks like:

    ```json
    {
        "detail": "Token is invalid or expired",
        "code": "token_not_valid"
    }
    ```
    """
    serializer_class = TokenVerifySerializer


class RefreshJSONWebToken(TokenRefreshView):
    """
    post:
    Refresh expired JSON Web Token.

    It is used JWT authentication with refresh expiration time = 14 days [Read JWT docs](https://jwt.io/). It
    means, that you have 14 days, from the time your token was generated, to update token with new one. So
    that you need to send your JSON WEB Token.

    ### Examples

    If data is successfully processed the server returns status code `200`.

    ```json
    {
        "refresh": "tgffemskdlgn3ksfngdDFHGergergEGRerRGEE346346vergd4232"
    }
    ```

    ### Errors

    If there were some error in client data, it sends status code `401` with the error message looks like:

    ```json
    {
        "detail": "Token is invalid or expired",
        "code": "token_not_valid"
    }
    ```
    """
    serializer_class = TokenRefreshSerializer


class SignUpView(CreateAPIView):
    """
    Register new user in the system

    You need to provide `email`, `first_name`, `last_name`, `password`. All the other information
    is additional
    """
    serializer_class = SignUpSerializer

    def perform_create(self, serializer):
        super().perform_create(serializer)
