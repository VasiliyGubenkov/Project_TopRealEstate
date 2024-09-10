from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Advert, AdvertDates
from .serializers import AdvertSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from .filters import AdvertFilter
from .models import Rating
from .serializers import RatingSerializer
from .filters import RatingFilter
from rest_framework.decorators import action
from django.contrib.auth.models import User


class AdvertViewSet(viewsets.ModelViewSet):
    queryset = Advert.objects.all()
    serializer_class = AdvertSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AdvertFilter
    ordering_fields = '__all__'
    ordering = ['title']
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        advert = serializer.save(owner=self.request.user)
        AdvertDates.objects.get_or_create(advert=advert)


class UserAdvertViewSet(viewsets.ModelViewSet):
    serializer_class = AdvertSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AdvertFilter
    ordering_fields = '__all__'
    ordering = ['title']

    def get_queryset(self):
        return Advert.objects.filter(owner=self.request.user)




class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#пример запроса: {"username": "newuser", "email": "newuser@example.com", "password": "password123", "password_confirm": "password123"}


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            csrf_token = get_token(request)
            return Response({
                'message': 'Login successful',
                'username': user.username,
                'csrf_token': csrf_token
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
#пример запроса {"email": "user@example.com","password": "yourpassword"}



class LogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not logged in'}, status=status.HTTP_400_BAD_REQUEST)
#отправляем ПУСТОЙ пост-запрос


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RatingFilter
    ordering_fields = '__all__'
    ordering = ['created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserRatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Rating.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'], url_path='myratings')
    def list_user_ratings(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
#Когда пользователь захочет отредактировать свой отзыв, ему нужно будет через слэш написать цифру обьявления, а не айди.
#Это логично, т.к. человек не может иметь два разных мнения по-поводу одной квартиры. Один обьект- один отзыв.


class AdvertDatesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        advert_dates_id = kwargs.get('id')
        try:
            advert_dates = AdvertDates.objects.get(id=advert_dates_id)
            advert_dates.update_dates()  # Обновляем даты перед отправкой
            advert_dates.save()
            return Response({'dates': advert_dates.dates}, status=status.HTTP_200_OK)
        except AdvertDates.DoesNotExist:
            return Response({'error': 'AdvertDates not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        advert_dates_id = kwargs.get('id')
        action = request.data.get('action')
        dates = request.data.get('dates', [])

        try:
            advert_dates = AdvertDates.objects.get(id=advert_dates_id)

            if action == 'add':
                advert_dates.add_dates(dates)
            elif action == 'remove':
                advert_dates.remove_dates(dates)
            else:
                return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

            advert_dates.update_dates()  # Обновляем даты после изменения
            advert_dates.save()
            return Response({'dates': advert_dates.dates}, status=status.HTTP_200_OK)
        except AdvertDates.DoesNotExist:
            return Response({'error': 'AdvertDates not found'}, status=status.HTTP_404_NOT_FOUND)