from django.shortcuts import render, redirect
from stores.models import Product
import random
from posts.models import *
from challenges.models import *
from stores.models import *
from django.db.models import Q, Count

def main(request):
    products = Product.objects.all()
    if len(products) >= 6:
        products = random.sample(list(products),6)
    context = {
        'products': products,
    }
    return render(request, 'main.html', context)

def search(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(Q(title__icontains=query) | Q(tags__name__icontains=query)).distinct()
        post_images = []
        for post in posts:
            p_images = PostImage.objects.filter(post=post)
            if p_images:
                post_images.append((post, p_images[0]))
            else:
                post_images.append((post,''))
        challenges = Challenge.objects.filter(Q(title__icontains=query)).distinct()
        challenge_images = []
        for challenge in challenges:
            c_images = ChallengeImage.objects.filter(challenge=challenge)
            if c_images:
                challenge_images.append((challenge, c_images[0]))
            else:
                challenge_images.append((challenge, ''))
        products = Product.objects.filter(Q(name__icontains=query)).distinct()
        product_images = []
        for product in products:
            pro_images = ProductImage.objects.filter(product=product)
            if pro_images:
                product_images.append((product, pro_images[0]))
            else:
                product_images.append((product, ''))
        context = {
            'query': query,
            'posts': post_images,
            'challenges': challenge_images,
            'products': product_images,
        }
    else:
        context = {}
    return render(request, 'search.html', context)