from django.contrib import admin
from .models import *

@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'address_city_name', 'address_street_name', 'address_house_number', 'price', 'number_of_rooms', 'type', 'owner', 'is_active')
    list_display_links = ('id', 'title', 'description', 'address_city_name', 'address_street_name', 'address_house_number', 'price', 'number_of_rooms', 'type', 'owner', 'is_active')
    search_fields = ('id', 'title', 'description', 'address_city_name', 'address_street_name', 'address_house_number', 'price', 'number_of_rooms', 'type', 'owner', 'is_active')
    list_filter = ('title',)
    ordering = ('title',)
    list_per_page = 20

@admin.register(AdvertDates)
class AdvertDatesAdmin(admin.ModelAdmin):
    list_display = ('advert', 'dates')
    list_display_links = ('advert', 'dates')
    search_fields = ('advert', 'dates')
    list_filter = ('advert', 'dates')
    ordering = ('advert',)
    list_per_page = 20
