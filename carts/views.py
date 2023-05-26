from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from stores.models import Product
import json

# @login_required
def cart_detail(request):
    is_logged_in = request.user.is_authenticated

    if is_logged_in:
        cart = Cart.objects.get(user=request.user)
        context = {'is_logged_in': is_logged_in, 'cart': cart}
    else:
        context = {'is_logged_in': is_logged_in}

    return render(request, 'carts/cart_detail.html', context)


@csrf_exempt
def add_item(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized access'})
    jsonObject = json.loads(request.body)
    product_id = int(jsonObject['product'])
    quantity = int(jsonObject['quantity'])

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'})

    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)

    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity

    cart_item.save()
    return JsonResponse({'success': 'Item added to cart'})