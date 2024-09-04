from django.urls import path, include
from . import api_views, html_views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('adverts', api_views.AdvertViewSet, basename='adverts')
app_name = 'main_app'


urlpatterns = [
    path('', html_views.start, name='start'),
    path('api/', include(router.urls)),

]