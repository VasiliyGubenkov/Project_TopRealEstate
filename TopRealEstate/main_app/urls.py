from django.urls import path, include
from . import api_views, html_views
from rest_framework.routers import DefaultRouter
from django.urls import path
from django.contrib.auth import views as auth_views


router = DefaultRouter()
router.register('adverts', api_views.AdvertViewSet, basename='adverts')
app_name = 'main_app'


urlpatterns = [
    path('', html_views.start, name='start'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/', include(router.urls)),

]

