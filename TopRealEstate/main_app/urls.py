from django.urls import path, include
from . import api_views, html_views
from rest_framework.routers import DefaultRouter
from .api_views import LoginAPIView, LogoutAPIView


router = DefaultRouter()
router.register('adverts', api_views.AdvertViewSet, basename='adverts')
router.register('myadverts', api_views.UserAdvertViewSet, basename='myadverts')
router.register('ratings', api_views.RatingViewSet, basename='ratings')
router.register('myratings', api_views.UserRatingViewSet, basename='myratings')
app_name = 'main_app'


urlpatterns = [
    path('', html_views.start, name='start'),
    path('registration/', api_views.UserRegistrationView.as_view(), name='user-registration'),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('api/', include(router.urls)),
    path('api/dates/<int:id>/', api_views.AdvertDatesAPIView.as_view(), name='advert-dates')
]

