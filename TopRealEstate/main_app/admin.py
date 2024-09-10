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

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('advert', 'owner', 'rating', 'review', 'updated_at')
    list_display_links = ('advert', 'owner')
    search_fields = ('advert__title', 'owner__username', 'review')
    list_filter = ('advert', 'owner', 'rating')
    ordering = ('-updated_at',)
    list_per_page = 20


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'advert', 'start_date', 'end_date', 'created_at')
    list_display_links = ('user', 'advert', 'start_date', 'end_date', 'created_at')
    search_fields = ('user', 'advert', 'start_date', 'end_date', 'created_at')
    list_filter = ('user', 'advert', 'start_date', 'end_date', 'created_at')
    ordering = ('user',)
    list_per_page = 20


@admin.register(BookLogging)
class BookLoggingAdmin(admin.ModelAdmin):
    list_display = ('user', 'advert')
    list_display_links = ('user', 'advert')
    search_fields = ('user', 'advert')
    list_filter = ('user', 'advert')
    ordering = ('user',)
    list_per_page = 20
