from rest_framework import serializers
from .models import Room

class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name')

class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
