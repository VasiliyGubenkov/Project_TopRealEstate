from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Advert
from .serializers import AdvertSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from .filters import AdvertFilter


class AdvertViewSet(viewsets.ModelViewSet):
    queryset = Advert.objects.all()
    serializer_class = AdvertSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AdvertFilter
    ordering_fields = '__all__'
    ordering = ['title']
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

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
#пример запроса: {"username": "your_username", "password": "your_password"}



class LogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not logged in'}, status=status.HTTP_400_BAD_REQUEST)
#отправляем ПУСТОЙ пост-запрос
