import django_filters
from .models import Advert
from .models import Rating


class AdvertFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')

    price = django_filters.RangeFilter(field_name='price', label="Цена (от и до)")

    address_city_name = django_filters.CharFilter(field_name='address_city_name', lookup_expr='icontains')
    address_street_name = django_filters.CharFilter(field_name='address_street_name', lookup_expr='icontains')
    address_house_number = django_filters.CharFilter(field_name='address_house_number', lookup_expr='icontains')

    class Meta:
        model = Advert
        fields = ['id', 'title', 'description', 'address_city_name', 'address_street_name',
                  'address_house_number', 'price', 'number_of_rooms', 'type', 'owner', 'is_active']

#/api/adverts/?price_min=1000&price_max=5000



class RatingFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(field_name='created_at', label="Дата создания (от и до)")
    advert_title = django_filters.CharFilter(field_name='advert__title', lookup_expr='icontains', label="Заголовок объявления")
    review = django_filters.CharFilter(field_name='review', lookup_expr='icontains', label="Отзыв (по ключевым словам)")

    class Meta:
        model = Rating
        fields = ['advert', 'rating', 'created_at', 'advert_title', 'review']
