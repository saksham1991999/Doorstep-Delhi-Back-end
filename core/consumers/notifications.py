import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Q

from core.models import Notification
from core.serializers import NotificationSerializer


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_group_name = 'notifications_%s' % self.user.username
        if self.user.username:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        data = await self.get_notifications(self.user)
        print(data)
        await self.channel_layer.group_add(
            'notifications',
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps(data))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive_json(self, text_data):
        if text_data['user'] != self.user.username:
            await self.send(text_data=json.dumps({
                'message': "Wrong User",
            }))
            await self.disconnect(403)
        else:
            if text_data['action'] == "dismiss":
                notification_id = text_data['notification_id']
                if await self.dismiss_notification(notification_id):
                    await self.send(text_data=json.dumps({
                        'message': "Notification Dismissed!",
                    }))
                else:
                    await self.send(text_data=json.dumps({
                        'message': "Wrong User",
                    }))

    async def send_to_websocket(self, event):
        await self.send_json(event)

    @database_sync_to_async
    def get_notifications(self, user):
        if self.user.username:
            notifications = Notification.objects.filter(Q(user=self.user) | Q(user=None), is_dismissed=False, is_promotional=False)
        else:
            notifications = Notification.objects.filter(user=None, is_dismissed=False, is_promotional=False)
        serializer = NotificationSerializer(notifications, many=True)
        return serializer.data

    async def send_notification(self, event):
        notification_id = event.get('notification_id')
        data = await self.get_notification(notification_id)
        await self.send_json(data)

    @database_sync_to_async
    def get_notification(self, id):
        notification = Notification.objects.filter(id=id)
        serializer = NotificationSerializer(notification, many=True)
        return serializer.data

    @database_sync_to_async
    def dismiss_notification(self, id):
        notification = Notification.objects.get(id=id)
        if notification.user == self.user:
            notification.is_dismissed = True
            notification.save()
            return True
        return False
