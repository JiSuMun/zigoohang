from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MinValueValidator, MaxValueValidator


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')
    title = models.CharField(max_length=50)
    content = RichTextUploadingField(blank=True, null=True)
    rating = models.DecimalField(default=0, max_digits=5, decimal_places=1)
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

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


class Review(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = RichTextUploadingField(blank=True,null=True)
    rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislike_reviews')


    def save(self, *args, **kwargs):
        self.post.rating = (self.post.rating*self.post.reviews.count() + self.rating) / (self.post.reviews.count() + 1)
        self.post.save()
        super(Review, self).save(*args, **kwargs)