import django_filters
from .models import Advert

class AdvertFilter(django_filters.FilterSet):
    # Настраиваем фильтрацию для полей title и description
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Advert
        fields = ['id', 'title', 'description', 'address_city_name', 'address_street_name',
                  'address_house_number', 'price', 'number_of_rooms', 'type', 'owner', 'is_active']