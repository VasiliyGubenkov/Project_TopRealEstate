from django.urls import path, include
from . import api_views, html_views
from rest_framework.routers import DefaultRouter
from .api_views import LoginAPIView, LogoutAPIView


router = DefaultRouter()
router.register('adverts', api_views.AdvertViewSet, basename='adverts')
app_name = 'main_app'


urlpatterns = [
    path('', html_views.start, name='start'),
    path('registration/', api_views.UserRegistrationView.as_view(), name='user-registration'),
    path('api/login/', LoginAPIView.as_view(), name='api-login'),
    path('api/logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('api/', include(router.urls)),
]

