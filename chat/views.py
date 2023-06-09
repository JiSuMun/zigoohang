from django.shortcuts import render, redirect, get_object_or_404
from .models import ChatRoom, Message, Notification
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.urls import reverse
from django.middleware.csrf import get_token

def inbox(request):
    chat_rooms = request.user.chat_rooms.all()
    chat_rooms_with_last_message = []
    all_users = get_user_model().objects.exclude(id=request.user.id)

    for chat_room in chat_rooms:
        unread_notifications = chat_room.notifications.filter(user=request.user, is_read=False).count()
        last_message = chat_room.messages.order_by('-timestamp').first()
        chat_rooms_with_last_message.append((chat_room, last_message, unread_notifications))

    context = {
        'chat_rooms': chat_rooms_with_last_message,
        'all_users': all_users,
        'user_username': request.user.username,
    }

    return render(request, 'chat/inbox.html', context)


def api_unread_notifications(request):
    user = request.user
    chat_rooms = user.chat_rooms.all()
    chat_rooms_data = []

    for chat_room in chat_rooms:
        unread_notifications = chat_room.notifications.filter(user=user, is_read=False).count()
        last_message = chat_room.messages.order_by('-timestamp').first()

        if last_message:
            last_message_content = last_message.content
            last_message_timestamp = last_message.formatted_timestamp()
        else:
            last_message_content = None
            last_message_timestamp = None

        chat_rooms_data.append({
            "room_id": chat_room.pk,
            "room_name": chat_room.name,
            "unread_notifications": unread_notifications,
            "last_message": last_message_content,
            "last_message_timestamp": last_message_timestamp,
        })
        print(chat_rooms_data)

    response_data = {
        "data": chat_rooms_data
    }

    return JsonResponse(response_data)


def start_chat(request, user_id):
    target_user = get_user_model().objects.get(id=user_id)
    chat_room = ChatRoom.get_or_create_chat_room([request.user, target_user])
    return redirect('chat:room', room_name=chat_room.name)


def start_group_chat(request):
    if request.method == 'POST':
        selected_user_ids = request.POST.getlist('user_ids')
        if selected_user_ids:
            selected_users = get_user_model().objects.filter(id__in=selected_user_ids)
            selected_users = list(selected_users) + [request.user]
            chat_room = ChatRoom.get_or_create_chat_room(selected_users)
            return redirect('chat:room', room_name=chat_room.name)
    return redirect('chat:inbox')


def room(request, room_name):
    chat_room = ChatRoom.objects.get(name=room_name)
    # chat_room = get_object_or_404(ChatRoom, name=room_name)
    messages = chat_room.messages.all()
    user = request.user
    unread_notifications = chat_room.notifications.filter(user=user, is_read=False)
    for notification in unread_notifications:
        notification.mark_as_read()

    context = {
        'room_name': room_name,
        'chat_room': chat_room,
        'messages': messages,
        'user': user,
    }
    return render(request, 'chat/room.html', context)


def delete_chat(request, room_name):
    chat_room = ChatRoom.objects.get(name=room_name)
    chat_room.delete()
    return redirect('chat:inbox')


def get_notifications(request):
    chat_rooms = request.user.chat_rooms.all()
    print(chat_rooms)
    unread_notifications = {}
    last_messages = {}

    for chat_room in chat_rooms:
        unread_notifications[chat_room.id] = chat_room.notifications.filter(user=request.user, is_read=False).count()
        last_message = chat_room.messages.order_by('-timestamp').first()
        if last_message:
            last_messages[chat_room.id] = {
                'content': last_message.content,
                'formatted_timestamp': last_message.formatted_timestamp(),
            }

    return JsonResponse({
        'unread_notifications': unread_notifications,
        'last_messages': last_messages
    })

# def delete_chat(request, room_name):
#     chat_room = ChatRoom.objects.get(name=room_name)
#     if request.user in chat_room.participants.all():
#         chat_room.participants.remove(request.user)
#     if chat_room.participants.count() == 0:
#         chat_room.delete()

#     return redirect('chat:inbox')