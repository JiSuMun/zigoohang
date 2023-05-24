from django.shortcuts import render, redirect
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Post, Review, PostImage, ReviewImage
from .forms import PostForm, ReviewForm, PostImageForm, DeleteImageForm, ReviewImageForm, DeleteReviewImageForm
from django.http import JsonResponse
from utils.news import search_naver_news
import json

# @receiver(post_save, sender=Post)
# def add_points_on_post_creation(sender, instance, created, **kwargs):
#     if created:
#         instance.user.points += 100
#         instance.user.save()

# @receiver(post_delete, sender=Post)
# def subtract_points_on_post_deletion(sender, instance, **kwargs):
#     instance.user.points -= 100
#     instance.user.save()

def main(request):
    return render(request, 'posts/main.html')

def index(request):
    posts = Post.objects.all()
    context = {
        'posts' : posts,
    }
    return render(request, 'posts/index.html', context)


def news(request):
    keyword = "친환경"
    result = search_naver_news(keyword)
    result_json = json.loads(result)
    context = {'result': result_json}
    return render(request, 'posts/news.html', context)


def create(request):
    post_form = PostForm()
    image_form = PostImageForm()
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        tags = request.POST.get('tags').split(',')
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            for tag in tags:
                post.tags.add(tag.strip())
            for i in files:
                PostImage.objects.create(image=i, post=post)
            return redirect('posts:detail', post.pk)
    context = {
        'post_form': post_form,
        'image_form': image_form,
    }
    return render(request, 'posts/create.html', context)


def detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    reviews = post.reviews.all().order_by('-created_at')
    image_form = ReviewImageForm()
    review_form = ReviewForm()
    u_review_forms = []

    for review in reviews:
        u_review_form = (
            review,
            ReviewForm(instance=review),
            ReviewImageForm(instance=review.reviewimage_set.first()),
            DeleteReviewImageForm(review=review)
        )
        u_review_forms.append(u_review_form)

    context = {
        'post': post,
        'reviews': reviews,
        'image_form': image_form,
        'review_form': review_form,
        'u_review_forms': u_review_forms,
    }
    return render(request, 'posts/detail.html', context)


def likes(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
        is_liked = False
    else:
        post.like_users.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked,
        'likes_count': post.like_users.count(),
    }
    return JsonResponse(context)


def update(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    post_form = PostForm(request.POST, instance=post)
    if request.method == 'POST':
        files = request.FILES.getlist('image')
        delete_ids = request.POST.getlist('delete_images')
        delete_form = DeleteImageForm(post=post, data=request.POST)        
        if post_form.is_valid() and delete_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            post.tags.clear()
            tags = request.POST.get('tags').split(',')
            for tag in tags:
                post.tags.add(tag.strip())
            for delete_id in delete_ids:
                post.postimage_set.filter(pk=delete_id).delete()
            for i in files:
                PostImage.objects.create(image=i, post=post)
            return redirect('posts:detail', post.pk)
    else:
        post_form = PostForm(instance=post)
        delete_form = DeleteImageForm(post=post)
    if post.postimage_set.exists():
        image_form = PostImageForm(instance=post.postimage_set.first())
    else:
        image_form = PostImageForm()
    context = {
        'post': post,
        'post_form': post_form,
        'image_form': image_form,
        'delete_form': delete_form,
    }

    return render(request, 'posts/update.html', context)  


def delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user == post.user:
        post.delete()
    return redirect('posts:index')


def review_create(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    image_form = ReviewImageForm()
    review_form = ReviewForm()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        image_form = ReviewImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.post = post
            review.save()
            for i in files:
                ReviewImage.objects.create(image=i, review=review)
            return redirect('posts:detail', post_pk)

    context = {
        'review_form': review_form,
        'post': post,
        'image_form': image_form,
    }
    return render(request, 'posts/detail.html', context)


def review_update(request, post_pk, review_pk):
    post = Post.objects.get(pk=post_pk)
    review = Review.objects.get(pk=review_pk)
    u_review_form = ReviewForm(instance=review)
    u_image_form = ReviewImageForm()
    delete_form = DeleteReviewImageForm(review=review)
    if request.method == 'POST':
        u_review_form = ReviewForm(request.POST, instance=review)
        files = request.FILES.getlist('image')
        delete_ids = request.POST.getlist('delete_images')
        delete_form = DeleteReviewImageForm(review=review, data=request.POST)
        if u_review_form.is_valid() and delete_form.is_valid():
            review = u_review_form.save(commit=False)
            review.post = post
            review.user = request.user
            review.save()
            for delete_id in delete_ids:
                review.reviewimage_set.filter(pk=delete_id).delete()
            for i in files:
                ReviewImage.objects.create(image=i, review=review)
        return redirect('posts:detail', post.pk)
    if review.reviewimage_set.exists():
        u_image_form = ReviewImageForm(instance=review.reviewimage_set.first())
    else:
        u_image_form = ReviewImageForm()
    context = {
        'post': post,
        'review': review,
        'u_review_form': u_review_form,
        'u_image_form': u_image_form,
        'delete_form': delete_form,
    }
    return render(request, 'posts/detail.html', context)



def review_delete(request, post_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        review.delete()

    return redirect('posts:detail', post_pk)



def review_likes(request, post_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user in review.like_users.all():
        review.like_users.remove(request.user)
        r_is_liked = False
    else:
        review.like_users.add(request.user)
        r_is_liked = True
    context = {
        'r_is_liked': r_is_liked,
        'review_likes_count': review.like_users.count(),
        'r_is_disliked': request.user in review.dislike_users.all(),
        'review_dislikes_count': review.dislike_users.count(),
    }
    return JsonResponse(context)


def review_dislikes(request, post_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user in review.dislike_users.all():
        review.dislike_users.remove(request.user)
        r_is_disliked = False
    else:
        review.dislike_users.add(request.user)
        r_is_disliked = True
    context = {
        'r_is_disliked': r_is_disliked,
        'review_dislikes_count': review.dislike_users.count(),
        'r_is_liked': request.user in review.like_users.all(),
        'review_likes_count': review.like_users.count(),
    }
    return JsonResponse(context)