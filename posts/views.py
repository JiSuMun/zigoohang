from django.shortcuts import render
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Post

@receiver(post_save, sender=Post)
def add_points_on_post_creation(sender, instance, created, **kwargs):
    if created:
        instance.user.points += 100
        instance.user.save()

@receiver(post_delete, sender=Post)
def subtract_points_on_post_deletion(sender, instance, **kwargs):
    instance.user.points -= 100
    instance.user.save()

