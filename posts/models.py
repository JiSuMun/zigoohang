from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MinValueValidator, MaxValueValidator
from imagekit.models import ProcessedImageField
import os


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')
    title = models.CharField(max_length=50)
    content = models.TextField()
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kargs):
        images = self.postimage_set.all()
        for image in images:
            image.delete()
        super(Post, self).delete(*args, **kargs)

    # def save(self, *args, **kwargs):
    #     # 새로운 게시글 작성인지 확인
    #     if self._state.adding:
    #         self.user.points += 100
    #         self.user.save()
    #     super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     # Subtract points when a post is deleted
    #     self.user.points -= 100
    #     self.user.save()
    #     super().delete(*args, **kwargs)

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def post_image_path(instance, filename):
        return f'post/{instance.post.pk}/{filename}'
    image = ProcessedImageField(
        upload_to=post_image_path,
        blank=True, 
        null=True)
    
    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
            dir_path = os.path.dirname(os.path.join(settings.MEDIA_ROOT, self.image.name))
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
        super(PostImage, self).delete(*args, **kargs)


class Review(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislike_reviews')


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def review_image_path(instance, filename):
        return f'review/{instance.review.pk}/{filename}'
    image = ProcessedImageField(
        upload_to=review_image_path,
        blank=True, 
        null=True,  
        options={'quality':90},)
    
    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
        super(ReviewImage, self).delete(*args, **kargs)

    def save(self, *args, **kwargs):
        if self.id:
            old_post = ReviewImage.objects.get(id=self.id)
            if self.image != old_post.image:
                if old_post.image:
                    os.remove(os.path.join(settings.MEDIA_ROOT, old_post.image.name))
        super(ReviewImage, self).save(*args, **kwargs)


class Zero(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100, blank=True)