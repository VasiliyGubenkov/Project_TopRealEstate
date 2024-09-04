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
