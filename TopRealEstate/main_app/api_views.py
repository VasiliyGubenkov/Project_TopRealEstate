from datetime import datetime, timedelta
from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Advert, AdvertDates, Booking, BookLogging, Rating
from .serializers import AdvertSerializer, BookingSerializer, UserRegistrationSerializer, RatingSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from .filters import AdvertFilter, RatingFilter
from rest_framework.decorators import action
from django.contrib.auth.models import User
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
        context['request'] = self.request
        return context


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
                    end_date=end_date_obj)
                BookLogging.objects.get_or_create(
                    user=request.user,
                    advert=advert_dates.advert)
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


class OwnerBookingListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        owner_adverts = Advert.objects.filter(owner=request.user)
        bookings = Booking.objects.filter(advert__in=owner_adverts)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OwnerBookingDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        booking_id = kwargs.get('id')
        try:
            booking = Booking.objects.get(id=booking_id, advert__owner=request.user)
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found or you do not have permission to access it'},
                            status=status.HTTP_404_NOT_FOUND)
    def patch(self, request, *args, **kwargs):
        booking_id = kwargs.get('id')
        confirmation_status = request.data.get('confirmation_from_the_owner')
        if confirmation_status not in ['confirmed', 'denied']:
            return Response({'error': 'Invalid confirmation status'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            booking = Booking.objects.get(id=booking_id, advert__owner=request.user)
            if confirmation_status == 'denied':
                advert_dates = booking.advert.dates
                start_date = booking.start_date
                end_date = booking.end_date
                if advert_dates:
                    existing_dates = advert_dates.dates.split(',')
                else:
                    existing_dates = []
                date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
                date_range_strings = [date.strftime('%Y-%m-%d') for date in date_range]
                new_dates = sorted(set(existing_dates + date_range_strings))
                advert_dates.dates = ','.join(new_dates)
                advert_dates.save()
            booking.confirmation_from_the_owner = confirmation_status
            booking.save()
            return Response({'message': f'Booking {confirmation_status} successfully'}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found or you do not have permission to modify it'},
                            status=status.HTTP_404_NOT_FOUND)
#пример апи запроса на продверждение или отклонение брони {"confirmation_from_the_owner": "confirmed"  // или "denied"}


class MyRatingsListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        ratings = Rating.objects.filter(owner=user)
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyRatingDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        rating_id = kwargs.get('id')
        try:
            rating = Rating.objects.get(id=rating_id, owner=request.user)
            serializer = RatingSerializer(rating)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Rating.DoesNotExist:
            return Response({'error': 'Rating not found or you do not have permission to access it'},
                            status=status.HTTP_404_NOT_FOUND)
    def patch(self, request, *args, **kwargs):
        rating_id = kwargs.get('id')
        try:
            rating = Rating.objects.get(id=rating_id, owner=request.user)
            serializer = RatingSerializer(rating, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Rating.DoesNotExist:
            return Response({'error': 'Rating not found or you do not have permission to modify it'},
                            status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, *args, **kwargs):
        rating_id = kwargs.get('id')
        try:
            rating = Rating.objects.get(id=rating_id, owner=request.user)
            rating.delete()
            return Response({'message': 'Rating deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Rating.DoesNotExist:
            return Response({'error': 'Rating not found or you do not have permission to delete it'},
                            status=status.HTTP_404_NOT_FOUND)
#пример изменения рейтинга и содержания отзыва {"rating": 10,"review": "Великолепно!"}


class BookingDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        booking_id = kwargs.get('id')
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found or you do not have permission to access it'},
                            status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, *args, **kwargs):
        booking_id = kwargs.get('id')
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            if booking.confirmation_from_the_owner in [None, 'confirmed', 'Not Confirmed']:
                advert_dates = booking.advert.dates
                start_date = booking.start_date
                end_date = booking.end_date
                if advert_dates:
                    existing_dates = advert_dates.dates.split(',')
                    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
                    new_dates = existing_dates + [date.strftime('%Y-%m-%d') for date in date_range]
                    advert_dates.dates = ','.join(sorted(set(new_dates)))
                    advert_dates.save()
            booking.delete()
            return Response({'message': 'Booking deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found or you do not have permission to delete it'},
                            status=status.HTTP_404_NOT_FOUND)
