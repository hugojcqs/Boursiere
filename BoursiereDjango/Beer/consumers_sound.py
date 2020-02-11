import asyncio
import json

from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import *


class MessageSoundConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.channel_layer.group_add(
            'sound',
            self.channel_name
        )
        await self.send({'type': 'websocket.accept'})

    async def websocket_send(self, message):
        await self.send(message)

    async def websocket_receive(self, event):
        pass
