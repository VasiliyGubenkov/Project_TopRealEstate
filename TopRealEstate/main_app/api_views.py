from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Advert
from .serializers import AdvertSerializer
from .permissions import IsOwnerOrReadOnly


class AdvertViewSet(viewsets.ModelViewSet):
    queryset = Advert.objects.all()
    serializer_class = AdvertSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id', 'title', 'description', 'address_city_name', 'address_street_name', 'address_house_number', 'price', 'number_of_rooms', 'type', 'owner', 'is_active']
    ordering_fields = '__all__'
    ordering = ['title']
    permission_classes = [IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserAdvertViewSet(viewsets.ModelViewSet):
    serializer_class = AdvertSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Advert.objects.filter(owner=self.request.user)








# Первый вариант, это стобы оунер автоматически добавлялся в таблицу
# from django.shortcuts import render, redirect
# from .models import Advert
# from .forms import AdvertForm
#
# def create_advert(request):
#     if request.method == 'POST':
#         form = AdvertForm(request.POST)
#         if form.is_valid():
#             advert = form.save(commit=False)
#             advert.owner = request.user  # Устанавливаем владельца на текущего пользователя
#             advert.save()
#             return redirect('some_view_name')
#     else:
#         form = AdvertForm()
#     return render(request, 'template_name.html', {'form': form})

# Второй вариант с другой вьюшкой, чтобы оунер автоматически добавлялся в таблицу
# from django.views.generic.edit import CreateView
# from .models import Advert
#
# class AdvertCreateView(CreateView):
#     model = Advert
#     fields = ['title', 'description', 'address_city_name', 'address_street_name', 'address_house_number', 'price', 'number_of_rooms', 'type']
#
#     def form_valid(self, form):
#         form.instance.owner = self.request.user  # Устанавливаем владельца на текущего пользователя
#         return super().form_valid(form)
