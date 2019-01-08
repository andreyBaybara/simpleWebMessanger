import json
import redis
from django.conf import settings
from django.utils.timezone import now
from .models import User


class MessageData:
    def __init__(self, sender_id,  message, index):
        self.message = message
        self.sender_id = sender_id
        self.index = index + 1

    def export_json(self):
        return json.dumps({
            'sender': self.sender_id,
            'message': self.message,
            'datetime': now().isoformat(),
            'index': self.index
        })


class UserData:

    def __init__(self, mobile_phone):
        self.userObj = User.objects.get(mobile_phone=mobile_phone)
        self.pk = self.userObj.pk
        self.username = self.userObj.username
        self.mobile_phone = self.userObj.mobile_phone

    def export_json(self):
        return json.dumps({
            'pk': self.pk,
            'username': self.username,
            'mobile_phone': self.mobile_phone
        })

    def export_data(self):
        return {
            'pk': self.pk,
            'username': self.username,
            'mobile_phone': self.mobile_phone
        }


class MessagesStorage:
    redis = None

    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL)

    def get_chat_key(self, user1_id, user2_id):
        return '_'.join(
                map(
                    str, sorted((user1_id, user2_id))
                )
            )

    def chat_exists(self, user1_id, user2_id):
        chat_key = self.get_chat_key(user1_id, user2_id)
        if self.redis.exists(chat_key):
            return True
        return False

    def create_chat(self,  user1_mobile_phone, user2_mobile_phone):
        user1_data = UserData(user1_mobile_phone)
        user2_data = UserData(user2_mobile_phone)

        chat_key = self.get_chat_key(user1_data.pk, user2_data.pk)
        if not self.redis.exists(chat_key):
            self.redis.rpush(user1_data.pk, chat_key)
            self.redis.rpush(user2_data.pk, chat_key)
            self.redis.rpush(chat_key, json.dumps({
                'user1': user1_data.export_data(),
                'user2': user2_data.export_data(),
                'index': 0
            }))
        return chat_key

    def add_message_to_chat(self, chat_key, sender, message):
        if self.redis.exists(chat_key):
            index = json.loads(self.redis.lindex(chat_key, -1)).get('index')
        else:
            index = 0
        message_data = MessageData(sender, message, index).export_json()
        self.redis.rpush(chat_key, message_data)

    def get_user_messages(self, user_id):
        if self.redis.exists(user_id):
            chat_keys = self.redis.lrange(user_id, 0, -1)
            return {
                    chat_key.decode(): list(map(
                        json.loads,
                        self.redis.lrange(chat_key, 0, -1)
                    ))
                    for chat_key in chat_keys
            }
        return None
