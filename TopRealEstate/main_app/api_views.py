from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Advert
from .serializers import AdvertSerializer
from .permissions import IsOwnerOrReadOnly


# class AdvertViewSet(viewsets.ModelViewSet):
#     queryset = Advert.objects.all()
#     serializer_class = AdvertSerializer
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
#     filterset_fields = ['id', 'title', 'description', 'address_city_name', 'address_street_name', 'address_house_number', 'price', 'number_of_rooms', 'type', 'owner', 'is_active']
#     ordering_fields = '__all__'
#     ordering = ['title']
#     permission_classes = [IsOwnerOrReadOnly]
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


class AdvertViewSet(viewsets.ModelViewSet):
    queryset = Advert.objects.all()
    serializer_class = AdvertSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id', 'title', 'description', 'address_city_name', 'address_street_name',
                        'address_house_number', 'price', 'number_of_rooms', 'type', 'owner', 'is_active']
    ordering_fields = '__all__'
    ordering = ['title']
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserAdvertViewSet(viewsets.ModelViewSet):
    serializer_class = AdvertSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Advert.objects.filter(owner=self.request.user)

