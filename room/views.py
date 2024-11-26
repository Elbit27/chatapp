from .models import Room
from . import serializers
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions, generics
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'room/rooms.html', {'rooms': rooms})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]
    return render(request, 'room/room.html', {'room': room, 'messages': messages})





class RoomViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Room.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RoomListSerializer
        return serializers.RoomDetailSerializer



class RoomCreateView(generics.CreateAPIView):
    serializer_class = serializers.RoomCreateSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save()