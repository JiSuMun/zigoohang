from django.shortcuts import render, redirect
from .models import S_Product, S_ProductImage, S_Purchase, S_Sales
from .forms import S_ProductForm, S_ProductImageForm, S_DeleteImageForm
from utils.map import get_latlng_from_address
import os
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import math

@login_required(login_url='accounts:login')

def index(request):
    products = S_Product.objects.all()
    no_status_products = S_Product.objects.filter(status='')
    reserved_products = S_Product.objects.filter(status='예약중')
    in_progress_products = S_Product.objects.filter(status='거래중')
    completed_products = S_Product.objects.filter(status='거래완료')

    u_address = request.user.address
    u_latitude, u_longitude = get_latlng_from_address(u_address)

    products_with_distance = []
    for product in products:
        product_address = product.road_address
        latitude, longitude = get_latlng_from_address(product_address)
        distance = calculate_distance(latitude, longitude, u_latitude, u_longitude)
        products_with_distance.append((product, distance))

    products_with_distance_sorted = sorted(products_with_distance, key=lambda x: x[1])

    context = {
        'products' : products,
        'no_status_products': no_status_products,
        'reserved_products': reserved_products,
        'in_progress_products': in_progress_products,
        'completed_products': completed_products,
        'products_with_distance': products_with_distance,
        'products_with_distance_sorted': products_with_distance_sorted,
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
            road_address = request.POST.get('road_address')
            split_address = address.split(' ')
            city = split_address[0]
            d_address = ' '.join(split_address[:3])
            product.address = address
            product.road_address = road_address
            product.d_address = d_address
            product.city = city
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
            road_address = request.POST.get('road_address')
            split_address = address.split(' ')
            city = split_address[0]
            d_address = ' '.join(split_address[:3])
            product.address = address
            product.road_address = road_address
            product.d_address = d_address
            product.city = city
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


def delete(request, product_pk):
    product = S_Product.objects.get(pk=product_pk)
    if request.user == product.user:
        product.delete()
    return redirect('secondhands:index')


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371 
    lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat/2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c

    return round(distance)


def detail(request, product_pk):
    product = S_Product.objects.get(pk=product_pk)
    d_address = product.d_address
    address = product.address
    road_address = product.road_address
    extra_address = product.extra_address
    latitude, longitude = get_latlng_from_address(road_address)
    u_address = request.user.address
    kakao_script_key = os.getenv('kakao_script_key')
    u_latitude, u_longitude = get_latlng_from_address(u_address)
    distance = calculate_distance(latitude, longitude, u_latitude, u_longitude)
    kakao_key = os.getenv('KAKAO_KEY')

    if address:
        s_address = address + ' ' + extra_address
    else:
        s_address = road_address + ' ' + extra_address

    context = {
        'kakao_script_key': kakao_script_key,
        'kakao_key': kakao_key,
        'product': product,
        'latitude': latitude,
        'longitude': longitude,
        'address': address,
        'extra_address': extra_address,
        's_address': s_address,
        'u_latitude': u_latitude,
        'u_longitude': u_longitude,
        'distance': distance,
        'd_address': d_address,
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


@login_required
def change_status(request, product_id, new_status):
    product = S_Product.objects.get(id=product_id)

    if request.user != product.user:
        return JsonResponse({'message': '권한이 없습니다.'}, status=403)

    product.status = new_status
    product.save()

    response_data = {'result': 'success', 'newStatus': product.get_status_display()}
    return JsonResponse(response_data)
