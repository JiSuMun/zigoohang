from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import os

class Challenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='participate_users')
    # superuser만 등록하게 하려면 코드 추가해야하나 테스트 편의성을 위해 나중 추가
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

class ChallengeImage(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)

    def challenge_image_path(instance, filename):
        return f'challenge/{instance.challenge.pk}/{filename}'
    image = ProcessedImageField(
            upload_to=challenge_image_path,
            blank=True, 
            null=True)
    
    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
            dir_path = os.path.dirname(os.path.join(settings.MEDIA_ROOT, self.image.name))
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
        super(ChallengeImage, self).delete(*args, **kargs)


class Certification(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='certifications')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def certification_image_path(instance, filename):
        return f'certification/{instance.user.username}/{filename}'
    image = ProcessedImageField(
            upload_to=certification_image_path,
            blank=True, 
            null=True)
    
