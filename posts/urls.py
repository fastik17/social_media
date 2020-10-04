from rest_framework.routers import DefaultRouter

from posts import views

app_name = 'posts'


router = DefaultRouter()

router.register('', views.PostViewSet,  basename='posts')


urlpatterns = [

] + router.urls
