import json
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from . import redis_storage as rstorage


class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        msgs_store = rstorage.MessagesStorage()
        user_chats = msgs_store.get_user_messages(request.user.pk)
        return render(request, 'chat/room.html', {
            'username': mark_safe(json.dumps(request.user.username)),
            'user_chats': user_chats,
            'user_pk': str(request.user.pk)
        })


@method_decorator(csrf_exempt, name='dispatch')
class AddFriendView(View):

    def post(self, request):
        try:
            new_friend_data = rstorage.UserData(request.POST.get('new_friend_phone'))
            adding_user_data = rstorage.UserData(request.POST.get('adding_user_phone'))
            msgs_store = rstorage.MessagesStorage()
        except ObjectDoesNotExist as err:
            return JsonResponse({
                'status': 'fail',
                'messages': err.args
            })
        if not msgs_store.chat_exists(new_friend_data.pk, adding_user_data.pk):
            chat_key = msgs_store.create_chat(new_friend_data.mobile_phone, adding_user_data.mobile_phone)
            return JsonResponse({
                'status': 'created',
                'chat_key': chat_key,
                'new_friend_data': new_friend_data.export_data(),
                'messages': []
            })
        chat_key = msgs_store.get_chat_key(new_friend_data.pk, adding_user_data.pk)
        return JsonResponse({
            'status': 'fail',
            'chat_key': chat_key,
            'new_friend_data': new_friend_data.export_data(),
            'messages': ['chat already exists']
        })

