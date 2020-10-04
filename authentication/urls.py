from django.urls import path

from authentication import views

app_name = 'auth'

urlpatterns = [
    path('', views.ObtainJSONWebToken.as_view(), name='auth'),
    path('verify/', views.VerifyJSONWebToken.as_view(), name='auth-verify'),
    path('refresh/', views.RefreshJSONWebToken.as_view(), name='auth-refresh'),
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
]
