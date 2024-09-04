from rest_framework import serializers
from .models import Advert


class AdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advert
        fields = '__all__'

