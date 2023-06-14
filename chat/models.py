from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone


class ChatRoom(models.Model):
    participants = models.ManyToManyField(get_user_model(), related_name='chat_rooms')
    name = models.CharField(max_length=255, blank=True)

    @classmethod
    def get_or_create_chat_room(cls, users):
        unique_users = set(users)
        if len(unique_users) == 1:
            room_name = "ME_Chat_with_" + list(unique_users)[0].username
        else:
            room_name = "Chat_with_" + "_".join(sorted([user.username for user in users]))

        chat_room = cls.objects.filter(name=room_name).first()
        if chat_room:
            return chat_room

        chat_room = cls.objects.create(name=room_name)
        chat_room.participants.set(unique_users)
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
        # self.timestamp에 대해 시간대 정보를 추가합니다.
        if self.timestamp.tzinfo is None or self.timestamp.tzinfo.utcoffset(self.timestamp) is None:
            local_timestamp = timezone.make_aware(self.timestamp, timezone.get_default_timezone())
        else:
            local_timestamp = self.timestamp

        am_pm = "오전" if local_timestamp.strftime('%p') == "AM" else "오후"
        return f"{am_pm} {local_timestamp.strftime('%I:%M')}"
    

class Notification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
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

    @classmethod
    def delete_old_notifications(cls):
        one_week_ago = timezone.now() - timezone.timedelta(days=7)
        cls.objects.filter(timestamp__lt=one_week_ago).delete()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.delete_old_notifications()
