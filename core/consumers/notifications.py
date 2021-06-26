import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_group_name = 'notification_%s' % self.user.username

        if self.user.is_authenticated():
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            await self.send(text_data=json.dumps({
                'message': "Accepted",
            }))
        else:
            await self.send(text_data=json.dumps({
                'message': "User Not Authenticated",
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
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_to_websocket',
                'message_type': 'text',
                'message': self.message,
                'sender': self.user.username,
            }
        )

    async def send_to_websocket(self, event):
        await self.send_json(event)

    async def send_notification(self, event):
        print(event)
        print("sending Notification")
        data = json.loads(event.get('value'))
        await self.send_json(data)
