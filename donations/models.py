from django.db import models
from django.utils import timezone
from django.conf import settings

class Donation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.user.subtract_points(self.amount)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Donation by {self.user.username}: {self.amount} points"