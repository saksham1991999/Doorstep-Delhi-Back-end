import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from room.models import Room, RoomUser, Message
from accounts.models import User


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope["user"]
        self.room = await get_room(self.room_name)
        self.room_user = await get_room_user(self.room, self.user)
        self.room_group_name = 'chat_%s' % self.room_name

        if self.room_user:
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            self.room_username_list = await get_room_username_list(self.room)
            await self.send(text_data=json.dumps({
                'message': "Accepted",
            }))
        else:
            await self.send(text_data=json.dumps({
                'message': "Wrong User or Room ID",
            }))
            await self.disconnect(403)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive_json(self, text_data):
        if (text_data['sender'] != self.user.username) or (str(text_data['room_id']) != str(self.room.id)):
            await self.send(text_data=json.dumps({
                'message': "Wrong Username or Room ID",
            }))
            await self.disconnect(403)

        message_type = text_data['message_type']
        if message_type == "text":
            self.message = text_data['message']
            room_id = text_data['room_id']
            time = await save_message(self.room,
                                      self.user,
                                      self.message,
                                      )
            time = time.strftime("%d %b %Y %H:%M:%S %Z")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_to_websocket',
                    'message_type': 'text',
                    'message': self.message,
                    'date_created': time,
                    'sender': self.user.username,
                    'room_id': room_id,
                }
            )

    async def send_to_websocket(self, event):
        await self.send_json(event)

@database_sync_to_async
def get_room(name):
    room = Room.objects.filter(name=name)[0]
    return room

@database_sync_to_async
def get_room_user(room, user):
    room_user = RoomUser.objects.filter(room=room, user=user)
    if room_user.exists():
        return room_user[0]
    return None

@database_sync_to_async
def get_room_username_list(room):
    room_users = room.users.values_list('username', flat=True)
    return room_users


@database_sync_to_async
def save_message(room, sender, text):
    user = User.objects.get(username = sender)
    new_message = Message(room=room, user=user, message_text=text)
    new_message.save()
    return new_message.created_on

