from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q, Count, Max
from django.utils import timezone


class ChatRoom(models.Model):
    participants = models.ManyToManyField(get_user_model(), related_name='chat_rooms')
    name = models.CharField(max_length=255, blank=True)

    @classmethod
    def get_or_create_chat_room(cls, user1, user2):
        user1_name = user1.username
        user2_name = user2.username

        if user1_name > user2_name:
            user1_name, user2_name = user2_name, user1_name

        if user1 == user2:
            chat_room = cls.objects.filter(name=f"ME_Chat_with_{user1_name}").first()
            if chat_room:
                return chat_room

            chat_room = cls.objects.create(name=f"ME_Chat_with_{user1_name}")
            chat_room.participants.set([user1])
            return chat_room

        chat_room = cls.objects.filter(participants__in=[user1, user2]).annotate(num_participants=Count('participants')).filter(num_participants=2).first()

        if chat_room:
            return chat_room

        chat_room = cls.objects.create(name=f"Chat_with_{user1_name}_and_{user2_name}")
        chat_room.participants.set([user1, user2])
        return chat_room


    def __str__(self):
        return self.name


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save()

    def formatted_timestamp(self):
        local_timestamp = timezone.localtime(self.timestamp)
        am_pm = "오전" if local_timestamp.strftime('%p') == "AM" else "오후"
        return f"{local_timestamp.strftime('%Y.%m.%d')} {am_pm} {local_timestamp.strftime('%I:%M')}"