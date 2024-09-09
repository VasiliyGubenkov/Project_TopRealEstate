from rest_framework import serializers
from .models import Advert
from django.contrib.auth.models import User
from .models import Advert, Rating


class AdvertSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    class Meta:
        model = Advert
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords must match"})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['advert', 'owner', 'rating']

