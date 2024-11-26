import os
import django
from rest_framework.generics import get_object_or_404

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message, Room
from django.contrib.auth.models import User

from django.http import Http404

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add (
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()


    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, room, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room': room,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room': room,
        }))

    @sync_to_async
    def save_message(self, username, room, message):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404(f"User with username {username} not found.")

        try:
            room = Room.objects.get(slug=room)
        except Room.DoesNotExist:
            raise Http404(f"Room with slug {room} not found.")

        Message.objects.create(user=user, room=room, content=message)