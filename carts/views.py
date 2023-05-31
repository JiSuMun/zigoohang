from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order, OrderItem
from stores.models import Product
from django.http import JsonResponse
import json

def cart_detail(request):

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        context = {'cart': cart}
    else:
        context = { }

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


def product_info(request, product_id):
    product = Product.objects.get(pk=product_id)
    image = product.images.first()
    print(product)
    print(image.image.url)
    data = {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'image': image.image.url,
    }
    return JsonResponse(data)


def order_page(request):
    # order = Order()
    # order.customer = request.user

    # products = request.POST.getlist('product_check')
    # # order.save()

    # for i in products:
    #     orderitem = OrderItem()
    #     orderitem.order = order
    #     product = Product.objects.get(pk=i)
    #     orderitem.product = product
    #     orderitem.quantity = 1
    #     orderitem.save()
    #     # print(i)

    # context = {
    #     'products': products,
    #     'order': order,
    # }

    # user = request.user
    # 상품 ID와 수량 정보
    product_ids = request.POST.getlist('product_check')
    quantities = request.POST.getlist('input_quantity')

    # products 딕셔너리를 생성해 값을 저장합니다.
    products = []
    total = 0
    for i, product_id in enumerate(product_ids):        
        product = Product.objects.get(pk=product_id)
        quantity = int(quantities[i])
        sub_total = product.price * quantity
        total += sub_total

        products.append({
            'product': product,
            'quantity': quantity,
            'sub_total': sub_total,
        })

    context = {
        'products': products,
        'total': total,
    }

    return render(request, 'carts/order_page.html', context)


def kakaopay(request):
    domain = request.get_host()
    context = {
        'domain': domain,
    }
    return render(request, 'payments/kakaopay.html', context)
    # return redirect(next_url)
def kakaopay_success(request):
    pass
def kakaopay_fail(request):
    pass
def kakaopay_cancel(request):
    pass