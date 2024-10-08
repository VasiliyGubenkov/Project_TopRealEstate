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
            password=validated_data['password'])
        return user


class RatingSerializer(serializers.ModelSerializer):
    advert = serializers.PrimaryKeyRelatedField(queryset=Advert.objects.none())
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Rating
        fields = ['id', 'advert', 'owner', 'rating', 'review', 'updated_at']
        read_only_fields = ['owner', 'updated_at']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context.get('request').user if 'request' in self.context else None
        if user and not self.instance:
            self.fields['advert'].queryset = Advert.objects.filter(
                id__in=BookLogging.objects.filter(user=user).values_list('advert_id', flat=True))
    def create(self, validated_data):
        request = self.context.get('request')
        if request is None:
            raise serializers.ValidationError({"request": "Request context is required but missing"})
        user = request.user
        advert = validated_data.get('advert')
        if Rating.objects.filter(owner=user, advert=advert).exists():
            raise serializers.ValidationError({"advert": "You have already rated this advert."})
        rating = Rating.objects.create(owner=user, **validated_data)
        rating.advert.update_average_rating()
        return rating


class BookingSerializer(serializers.ModelSerializer):
    owner_of_advert = serializers.ReadOnlyField(source='advert.owner.id')
    confirmation_from_the_owner = serializers.ChoiceField(choices=[('null', 'Null'), ('confirmed', 'Confirmed'), ('denied', 'Denied')], default='null')
    class Meta:
        model = Booking
        fields = ['id', 'user', 'advert', 'start_date', 'end_date', 'created_at', 'owner_of_advert', 'confirmation_from_the_owner']
        read_only_fields = ['user', 'created_at', 'owner_of_advert', 'confirmation_from_the_owner']
