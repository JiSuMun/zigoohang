from django.db import models
from django.conf import settings
from django.db.models import Max
from django.contrib.auth import get_user_model


class ChatRoom(models.Model):
    participants = models.ManyToManyField(get_user_model(), related_name='chat_rooms')
    name = models.CharField(max_length=255, blank=True)

    @classmethod
    def get_or_create_chat_room(cls, user1, user2):
        chat_room = cls.objects.filter(participants=user1).filter(participants=user2).first()
        if not chat_room:
            chat_room = cls.objects.create()
            chat_room.participants.add(user1, user2)
            chat_room.set_default_name(user1, user2)
        return chat_room

    def set_default_name(self, user1, user2):
        self.name = f"Chat_with_{user1.username}_and_{user2.username}" 
        self.save()
    

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