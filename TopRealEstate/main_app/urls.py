from django.urls import path, include
from . import api_views, html_views


app_name = 'main_app'


urlpatterns = [
    path('', html_views.start, name='start'),

]