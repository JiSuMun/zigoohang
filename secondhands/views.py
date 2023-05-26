from django.shortcuts import render, redirect
from .models import S_Product, S_ProductImage, S_Purchase, S_Sales
from .forms import S_ProductForm, S_ProductImageForm, S_DeleteImageForm
from utils.map import get_latlng_from_address
import os
from django.http import JsonResponse


def index(request):
    products = S_Product.objects.all()
    context = {
        'products' : products,
    }
    return render(request, 'secondhands/index.html', context)


def create(request):
    product_form = S_ProductForm()
    image_form = S_ProductImageForm()
    if request.method == 'POST':
        product_form = S_ProductForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            address = request.POST.get('address')
            product.address = address
            product.save()
            for i in files:
                S_ProductImage.objects.create(image=i, product=product)
            return redirect('secondhands:detail', product.pk)
    context = {
        'product_form': product_form,
        'image_form': image_form,
    }
    return render(request, 'secondhands/create.html', context)


def update(request, product_pk):
    product = S_Product.objects.get(pk=product_pk)
    if request.method == 'POST':
        product_form = S_ProductForm(request.POST, instance=product)
        files = request.FILES.getlist('image')
        delete_ids = request.POST.getlist('delete_images')
        delete_form = S_DeleteImageForm(product=product, data=request.POST)        
        if product_form.is_valid() and delete_form.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            address = request.POST.get('address')
            product.address = address
            product.save()
            for delete_id in delete_ids:
                product.s_productimage_set.filter(pk=delete_id).delete()
            for i in files:
                S_ProductImage.objects.create(image=i, product=product)
            return redirect('secondhands:detail', product.pk)
    else:
        product_form = S_ProductForm(instance=product)
        delete_form = S_DeleteImageForm(product=product)
    if product.s_productimage_set.exists():
        image_form = S_ProductImageForm(instance=product.s_productimage_set.first())
    else:
        image_form = S_ProductImageForm()
    context = {
        'product': product,
        'product_form': product_form,
        'image_form': image_form,
        'delete_form': delete_form,
    }

    return render(request, 'secondhands/update.html', context)  


def delete(request, post_pk):
    product = S_Product.objects.get(pk=post_pk)
    if request.user == product.user:
        product.delete()
    return redirect('secondhands:index')


def detail(request, product_pk):
    product = S_Product.objects.get(pk=product_pk)
    address = product.address
    extra_address = product.extra_address
    latitude, longitude = get_latlng_from_address(address)
    kakao_script_key = os.getenv('kakao_script_key')
    kakao_key = os.getenv('kakao_key')
    s_address = address + extra_address
    context = {
        'kakao_script_key': kakao_script_key,
        'kakao_key': kakao_key,
        'product': product,
        'latitude': latitude,
        'longitude': longitude,
        'address': address,
        'extra_address': extra_address,
        's_address': s_address,
    }
    return render(request, 'secondhands/detail.html', context)


def likes(request, product_pk):
    product = S_Product.objects.get(pk=product_pk)
    if request.user in product.like_users.all():
        product.like_users.remove(request.user)
        is_liked = False
    else:
        product.like_users.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked,
        'likes_count': product.like_users.count(),
    }
    return JsonResponse(context)