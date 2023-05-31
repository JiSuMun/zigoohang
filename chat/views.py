from django.shortcuts import render, redirect
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model
from django.db.models import Q, Count


def inbox(request):
    chat_rooms = request.user.chat_rooms.all()
    return render(request, 'chat/inbox.html', {'chat_rooms': chat_rooms})


def start_chat(request, user_id):
    user = get_user_model().objects.get(id=user_id)
    chat_room = ChatRoom.get_or_create_chat_room(request.user, user)
    chat_room.set_default_name(request.user, user)
    return redirect('chat:room', room_name=chat_room.name)


def room(request, room_name):
    chat_room = ChatRoom.objects.get(name=room_name)
    messages = chat_room.messages.all()
    context = {
        'room_name': room_name,
        'chat_room': chat_room,
        'messages': messages
    }
    return render(request, 'chat/room.html', context)


def delete_chat(request, room_name):
    chat_room = ChatRoom.objects.get(name=room_name)

    if request.user in chat_room.participants.all():
        chat_room.participants.remove(request.user)

    if chat_room.participants.count() == 0:
        chat_room.delete()

    return redirect('chat:inbox')



# def delete_chat(request, room_name):
#     chat_room = ChatRoom.objects.get(name=room_name)
#     chat_room.delete()
#     return redirect('chat:inbox')