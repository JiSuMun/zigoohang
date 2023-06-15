from django.shortcuts import render, redirect
from .models import Store, Product, ProductReview
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import *


##### stores
# store 나열
def index(request):
    stores = Store.objects.all()
    context = {
        'stores': stores,
    }
    return render(request, 'stores/index.html', context)


@login_required
def create(request):
    if not(request.user.is_seller or request.user.is_staff):
        return redirect('stores:index')
    if request.method == 'POST':
        store_form = StoreForm(request.POST, request.FILES)
        if store_form.is_valid():
            store = store_form.save(commit=False)
            store.user = request.user
            store.save()
            return redirect('stores:index')
    else:
        store_form = StoreForm()

    context = {
        'store_form': store_form,
    }
    return render(request, 'stores/create.html', context)


# 상품 나열
def detail(request, store_pk):
    products = Product.objects.filter(store=store_pk)
    store = Store.objects.get(pk=store_pk)
    context = {
        'products': products,
        'store': store,
    }
    return render(request, 'stores/detail.html', context)


@login_required
def update(request, store_pk):
    store = Store.objects.get(pk=store_pk)
    if not(request.user.is_seller or request.user.is_staff or request.user == store.user):
        return redirect('stores:index')
    if request.method == 'POST':
        store_form = StoreForm(request.POST, request.FILES, instance=store)
        if store_form.is_valid():
            store = store_form.save(commit=False)
            store.user = request.user
            store.save()
            return redirect('stores:index')
    else:
        store_form = StoreForm(instance=store)
    
    context = {
        'store_form': store_form,
        'store': store,
    }

    return render(request, 'stores/update.html', context)


@login_required
def delete(request, store_pk):
    store = Store.objects.get(pk=store_pk)
    if not(request.user.is_seller or request.user.is_staff or request.user == store.user):
        return redirect('stores:index')
    if request.user == store.user:
        store.delete()
    return redirect('stores:index')


##### products
@login_required
def products_create(request, store_pk):
    store = Store.objects.get(pk=store_pk)
    if not(request.user.is_seller or request.user.is_staff or request.user == store.user):
        return redirect('stores:index')
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.store = store
            product.save()
            for image in request.FILES.getlist('image'):
                ProductImage.objects.create(image=image, product=product) 
            return redirect('stores:products_detail', store.pk, product.pk)
    else:
        product_form = ProductForm()
        image_form = ProductImageForm()
    context = {
        'product_form': product_form,
        'image_form': image_form,
        'store': store,
    }
    return render(request, 'stores/products_create.html', context)


def products_detail(request, store_pk, product_pk):
    store = Store.objects.get(pk=store_pk)
    print(store)
    product = Product.objects.get(pk=product_pk)
    print(product)
    reviews = ProductReview.objects.filter(product=product)
    print(reviews)
    for review in reviews:
        review.review_images = [review.image1, review.image2, review.image3, review.image4, review.image5]
    context = {
        'store': store,
        'product': product,
        'reviews': reviews,
    }
    return render(request, 'stores/products_detail.html', context)


@login_required
def products_update(request, store_pk, product_pk):
    store = Store.objects.get(pk=store_pk)
    if not(request.user.is_seller or request.user.is_staff or request.user == store.user):
        return redirect('stores:index')
    product = Product.objects.get(pk=product_pk)
    images = product.images.all()
    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        if product_form.is_valid():
            product = product_form.save()
            for image in request.FILES.getlist('image'):
                ProductImage.objects.create(image=image, product=product)
            for image_pk in request.POST.getlist('delete_image'):
                ProductImage.objects.get(pk=image_pk).delete()
        return redirect('stores:products_detail', store.pk, product.pk)
    else:
        product_form = ProductForm(instance=product)
        image_form = ProductImageForm()
    context = {
        'product_form': product_form,
        'image_form': image_form,
        'store': store,
        'images': images,
    }

    return render(request, 'stores/products_update.html', context)


@login_required
def products_delete(request, store_pk, product_pk):
    product = Product.objects.get(pk=product_pk)
    if not(request.user.is_seller or request.user.is_staff or request.user == product.store.user):
        return redirect('stores:index')
    if request.user == product.store.user:
        product.delete()
    return redirect('stores:detail', store_pk)


@login_required
def products_likes(request, store_pk, product_pk):
    product = Product.objects.get(pk=product_pk)
    if product.like_users.filter(pk=request.user.pk).exists():
        product.like_users.remove(request.user)
        is_liked = False
    else:
        product.like_users.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked,
    }
    return JsonResponse(context)
    # return redirect('stores:products_detail', store_pk, product_pk)


##### reviews
@login_required
def reviews_create(request, store_pk, product_pk):
    product = Product.objects.get(pk=product_pk)
    if request.method == 'POST':
        review_form = ProductReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('stores:products_detail', store_pk, product.pk)
    else:
        review_form = ProductReviewForm()
    context = {
        'review_form': review_form,
        'product': product,
    }
    return render(request, 'stores/reviews_create.html', context)


@login_required
def reviews_update(request, store_pk, product_pk, review_pk):
    review = ProductReview.objects.get(pk=review_pk)
    if request.user != review.user:
        return redirect('stores:products_detail', review.product.store.pk, review.product.pk)
    # product = Product.objects.get(pk=product_pk)
    if request.method == 'POST':
        review_form = ProductReviewForm(request.POST, request.FILES, instance=review)
        if review_form.is_valid():
            review = review_form.save()
            return redirect('stores:products_detail', review.product.store.pk, review.product.pk)
    else:
        review_form = ProductReviewForm(instance=review)        
    context = {
        'review_form': review_form,
        'review': review,
    }
    return render(request, 'stores/reviews_update.html', context)


@login_required
def reviews_delete(request, store_pk, product_pk, review_pk):
    review = ProductReview.objects.get(pk=review_pk)
    if review.user == request.user:
        review.delete()
    return redirect('stores:products_detail', store_pk, product_pk )


@login_required
def reviews_likes(request, store_pk, product_pk, review_pk):
    review = ProductReview.objects.get(pk=review_pk)
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


@login_required
def reviews_dislikes(request, store_pk, product_pk, review_pk):
    review = ProductReview.objects.get(pk=review_pk)
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


##### cart

# def add_to_cart(request, product_id):
#     cart = request.session.get('cart', {})  # Retrieve the cart data from the session
#     quantity = cart.get(product_id, 0) + 1
#     cart[product_id] = quantity
#     request.session['cart'] = cart  # Store the updated cart data in the session under 'cart' key
#     return redirect('cart')


# def cart(request):
#     cart = request.session.get('cart', {})
#     product_ids = cart.keys()
#     products = Product.objects.filter(id__in=product_ids)
#     context = {'cart': cart, 'products': products}
#     return render(request, 'cart.html', context)


# def remove_from_cart(request, product_id):
#     cart = request.session.get('cart', {})
#     if product_id in cart:
#         del cart[product_id]
#         request.session['cart'] = cart  # Update the cart data in the session
#     return redirect('cart')


# def update_quantity(request, product_id):
#     cart = request.session.get('cart', {})
#     new_quantity = request.POST.get('quantity')  # Retrieve the new quantity from the request
#     if new_quantity:
#         cart[product_id] = int(new_quantity)
#         request.session['cart'] = cart  # Update the cart data in the session
#     return redirect('cart')
