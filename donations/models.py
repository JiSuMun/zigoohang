from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models import Sum


class Donation(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=100)

    # 기부를 하게 되면 기부포인트만큼 user의 포인트 빠짐
    def save(self, *args, **kwargs):
        self.user.subtract_points(self.amount)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Donation by {self.user.username}: {self.amount} points"
    
    def calculate_total_donations_by_name(name):
        total_amount = Donation.objects.filter(name=name).aggregate(total=Sum('amount'))['total']
        return total_amount or 0