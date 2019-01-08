from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import User
from . import redis_storage as rstorage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.message_storage = rstorage.MessagesStorage()
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.userObj = await self.get_user_obj(self.user_id)
        await self.channel_layer.group_add(
            self.user_id,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user_id,
            self.channel_name
        )

    @database_sync_to_async
    def save_message(self, chat_key, sender, message):
        self.message_storage.add_message_to_chat(chat_key, sender, message)

    @database_sync_to_async
    def get_user_obj(self, pk):
        return User.objects.get(pk=pk)

    async def get_receiver_id(self, chat_key):
        """split chat_key and check,
        if splitted part not equal to self.user id
        another part is receiver id"""

        item = chat_key.split('_')
        if self.user_id != item[0]:
            return item[0]
        return item[1]

    async def receive(self, text_data):
        data_json = json.loads(text_data)
        message = data_json['message']
        chat_key = data_json['chat_key']
        sender_id = self.user_id

        receiver_id = await self.get_receiver_id(chat_key)
        await self.save_message(chat_key, sender_id, message)

        # if message sended to yourself send only to yourself
        if receiver_id == sender_id:
            await self.channel_layer.group_send(
                receiver_id,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user_id': sender_id,
                    'receiver_id': receiver_id,
                    'chat_key': chat_key
                }
            )
        else:
            # if message sended to another user send this to user and yourself
            await self.channel_layer.group_send(
                receiver_id,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user_id': sender_id,
                    'receiver_id': receiver_id,
                    'chat_key': chat_key
                }
            )
            await self.channel_layer.group_send(
                self.user_id,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user_id': self.user_id,
                    'receiver_id': receiver_id,
                    'chat_key': chat_key
                }
            )

    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        receiver_id = event['receiver_id']
        chat_key = event['chat_key']
        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
            'receiver_id': receiver_id,
            'chat_key': chat_key
        }))
