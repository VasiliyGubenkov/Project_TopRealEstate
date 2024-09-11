from datetime import datetime, timedelta
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Advert, AdvertDates, Booking, BookLogging
from .serializers import AdvertSerializer, BookingSerializer
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
from rest_framework import serializers
from rest_framework.filters import OrderingFilter


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
        booked_adverts = BookLogging.objects.filter(user=self.request.user).values_list('advert', flat=True)
        return Advert.objects.filter(id__in=booked_adverts)




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
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RatingFilter
    ordering_fields = '__all__'
    ordering = ['updated_at']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        advert_dates_id = kwargs.get('id')
        try:
            advert_dates = AdvertDates.objects.get(id=advert_dates_id)
            return Response({'dates': advert_dates.dates}, status=status.HTTP_200_OK)
        except AdvertDates.DoesNotExist:
            return Response({'error': 'AdvertDates not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        advert_dates_id = kwargs.get('id')
        action = request.data.get('action')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        try:
            advert_dates = AdvertDates.objects.get(id=advert_dates_id)
            dates_list = advert_dates.dates.split(',')
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            if action == 'remove':
                new_dates = []
                for date_str in dates_list:
                    current_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    if current_date < start_date_obj or current_date > end_date_obj:
                        new_dates.append(date_str)
                advert_dates.dates = ','.join(new_dates)
                advert_dates.save()

                booking = Booking.objects.create(
                    user=request.user,
                    advert=advert_dates.advert,
                    start_date=start_date_obj,
                    end_date=end_date_obj
                )

                BookLogging.objects.get_or_create(
                    user=request.user,
                    advert=advert_dates.advert
                )
                return Response({'dates': advert_dates.dates}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        except AdvertDates.DoesNotExist:
            return Response({'error': 'AdvertDates not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

#пример удаления(бронирования) дат {"action": "remove", "start_date": "2024-09-10", "end_date": "2024-09-15"}



class UserBookingsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        bookings = Booking.objects.filter(user=user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






class BookingDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        booking_id = kwargs.get('id')
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found or you do not have permission to access it'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        booking_id = kwargs.get('id')
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            # Delete the booking
            advert_dates = AdvertDates.objects.get(advert=booking.advert)
            dates_list = advert_dates.dates.split(',')
            start_date = booking.start_date
            end_date = booking.end_date

            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.strftime('%Y-%m-%d')
                if date_str not in dates_list:
                    dates_list.append(date_str)
                current_date += timedelta(days=1)

            advert_dates.dates = ','.join(sorted(dates_list))
            advert_dates.save()

            BookLogging.objects.get_or_create(user=booking.user, advert=booking.advert)

            booking.delete()

            return Response({'message': 'Booking deleted and dates returned successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found or you do not have permission to delete it'}, status=status.HTTP_404_NOT_FOUND)
        except AdvertDates.DoesNotExist:
            return Response({'error': 'AdvertDates not found'}, status=status.HTTP_404_NOT_FOUND)
