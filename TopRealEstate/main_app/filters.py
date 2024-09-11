from .models import Advert, Rating
import django_filters


class AdvertFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
    price = django_filters.RangeFilter(field_name='price', label="Цена (от и до)")
    number_of_rooms = django_filters.RangeFilter(field_name='number_of_rooms', label="Количество комнат (от и до)")
    address_city_name = django_filters.CharFilter(field_name='address_city_name', lookup_expr='icontains')
    address_street_name = django_filters.CharFilter(field_name='address_street_name', lookup_expr='icontains')
    address_house_number = django_filters.CharFilter(field_name='address_house_number', lookup_expr='icontains')
    class Meta:
        model = Advert
        fields = ['id', 'title', 'description', 'address_city_name', 'address_street_name',
                  'address_house_number', 'price', 'number_of_rooms', 'type', 'is_active']


class RatingFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(field_name='updated_at', label="Дата создания (от и до)")
    advert_title = django_filters.CharFilter(field_name='advert__title', lookup_expr='icontains', label="Заголовок объявления")
    review = django_filters.CharFilter(field_name='review', lookup_expr='icontains', label="Отзыв (по ключевым словам)")
    class Meta:
        model = Rating
        fields = ['advert', 'rating', 'updated_at', 'advert_title', 'review']
