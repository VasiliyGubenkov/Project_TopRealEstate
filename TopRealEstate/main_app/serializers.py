from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Advert, Rating, Booking, BookLogging


class AdvertSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    class Meta:
        model = Advert
        fields = '__all__'
        read_only_fields = ('owner',)


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
        fields = ['advert', 'owner', 'rating', 'review', 'updated_at']
        read_only_fields = ['owner', 'updated_at']

    def save(self, **kwargs):
        advert = self.validated_data.get('advert')
        user = self.context['request'].user

        if not BookLogging.objects.filter(user=user, advert=advert).exists():
            raise serializers.ValidationError({"advert": "You can only rate adverts you have booked."})

        instance = super().save(**kwargs)
        instance.advert.update_average_rating()
        return instance



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['user', 'advert', 'start_date', 'end_date', 'created_at']



