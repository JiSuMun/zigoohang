from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order, OrderItem
from accounts.models import PointLog, PointLogItem
from stores.models import Product
from django.http import JsonResponse, HttpResponseNotFound
import os, requests, json, math

POINT_PER_PRICE = 0.01

def cart_detail(request):

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
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

    cart_count = user_cart.cartitems.count()
    return JsonResponse({'success': 'Item added to cart', 'cart_count': cart_count})


def modify_quantity(request):
    jsonObject = json.loads(request.body)
    product_pk = jsonObject['productId']
    quantityValue = int(jsonObject['quantityValue'])

    product = Product.objects.get(pk=product_pk)
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)
    print(product)
    if quantityValue == 1:
        cart_item.quantity += 1
    elif quantityValue == -1 and cart_item.quantity > 1:
        cart_item.quantity -= 1

    cart_item.save()
    context = {
        # 'product_pk': product_pk,
        # 'price': product.price,
        'quantity': cart_item.quantity,
        'subTotal': cart_item.sub_total(),
        'total': user_cart.total(),
        # 'user_cart': user_cart,
    }
    return JsonResponse(context)


def remove_item(request):
    jsonObject = json.loads(request.body)
    product_ids = jsonObject['productIds']
    # print(product_ids)
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    for i in product_ids:
        product = Product.objects.get(pk=i)
        cart_item = CartItem.objects.get(cart=user_cart, product=product)
        cart_item.delete()
        print(cart_item)
    data = {}
    return JsonResponse(data)
    # return redirect('carts:cart_detail')


# localstorage
def product_info(request, product_id):
    product = Product.objects.get(pk=product_id)
    image = product.images.first()
    print(product)
    print(image.image.url)
    data = {
        'id': product.id,
        'storeId': product.store.pk,
        'name': product.name,
        'price': product.price,
        'image': image.image.url,
    }
    return JsonResponse(data)


@login_required
def order_page(request):
    products = request.POST.getlist('item_check')
    quantities = request.POST.getlist('input_quantity')
    order = Order()
    order.customer = request.user
    order.seller = Product.objects.get(pk=products[0]).store.user
    order.save()

    print(order)
    
    for i, product_id in enumerate(products):
        orderitem = OrderItem()
        orderitem.order = order
        product = Product.objects.get(pk=product_id)
        orderitem.product = product
        orderitem.quantity = quantities[i]
        orderitem.save()

    context = {
        # 'products': products,
        'order': order,
    }

    return render(request, 'carts/order_page.html', context)


# def kakaopay(request):
#     order_id = request.POST.get('order_id')
#     order = Order.objects.get(pk=order_id)
#     domain = request.get_host()
#     cnt = 0
#     order_item = 'none'
#     for item in order.order_items.all():
#         cnt += 1
#         if cnt == 1:
#             order_item = item.product.name
#     if cnt > 1:
#         order_item += f' 외 {cnt-1} 건'

#     URL = 'https://kapi.kakao.com/v1/payment/ready'
#     headers = {
#         'Authorization': 'KakaoAK ' + KAKAO_AK,
#     }
#     params = {
#         'cid': 'TC0ONETIME',    # 테스트용 코드
#         'partner_order_id': order_id,     # 주문번호
#         'partner_user_id': request.user.username, # 유저 아이디
#         'item_name': order_item,        # 구매 물품 이름
#         'quantity': cnt,                # 구매 물품 수량
#         'total_amount': order.total(),        # 구매 물품 가격
#         'tax_free_amount': '0',         # 구매 물품 비과세
#         'approval_url': f'http://{domain}/carts/kakaopay/approval/{order_id}/', # 결제 승인시 이동할 url
#         'cancel_url': f'http://{domain}/carts/kakaopay/cancel/', # 결제 취소 시 이동할 url
#         'fail_url': f'http://{domain}/carts/kakaopay/fail/', # 결제 실패 시 이동할 url
#     }

#     res = requests.post(URL, headers=headers, params=params)
#     request.session['tid'] = res.json()['tid']      # 결제 승인시 사용할 tid를 세션에 저장
#     next_url = res.json()['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장
#     return redirect(next_url)
#     # return render(request, 'payments/kakaopay.html', context)


# def kakaopay_approval(request, order_id):
#     url = 'https://kapi.kakao.com/v1/payment/approve'
#     headers = {
#         'Authorization': f'KakaoAK {KAKAO_AK}',
#     }
#     params = {
#         'cid':'TC0ONETIME',
#         'tid': request.session['tid'], #결제 고유 번호
#         'partner_order_id': order_id, #주문 번호
#         'partner_user_id': request.user.username, #유저 아이디
#         'pg_token': request.GET['pg_token'] # 쿼리 스트링으로 받은 pg토큰
#     }
#     res = requests.post(url, headers=headers, params=params)
#     result = res.json()
#     print(dir(result))
#     context = {
#         'result': result,
#     }
#     return render(request, 'payments/kakaopay_approval.html', context)


# def kakaopay_cancel(request):
#     context = {
#     }
#     return render(request, 'payments/kakaopay_cancel.html', context)


# def kakaopay_fail(request):
#     context = {
#     }
#     return render(request, 'payments/kakaopay_fail.html', context)

def approval(request):
    jsonObject = json.loads(request.body)
    print(jsonObject)
    order_id = int(jsonObject['orderId'])

    order = Order.objects.get(pk=order_id)
    order.pay_type = jsonObject['pg']
    order.postcode = jsonObject['orderPostcode']
    order.address = jsonObject['orderAddress']
    order.phone = jsonObject['orderPhone']
    order.email = jsonObject['orderEmail']
    order.memo = jsonObject['orderMsg']
    order.receiver = jsonObject['receiver']
    order.total_price = int(jsonObject['totalAmount'])
    order.use_points = int(jsonObject['usePoints'])
    order.total_amount = int(jsonObject['finalAmount'])

    order.shipping_status='배송준비중'
    order.save()

    user_cart, created = Cart.objects.get_or_create(user=request.user)
    for order_item in order.order_items.all():
        product_pk = order_item.product.pk
        matching_cart_items = user_cart.cartitems.filter(product__pk=product_pk)
    
        for cart_item in matching_cart_items:
            cart_item.delete()
            
    if request.user.is_authenticated:
        real_point = int((int(jsonObject['totalAmount']) - int(jsonObject['usePoints'])) * POINT_PER_PRICE)
        user = request.user
        user.total_points += real_point
        # user.points += real_point
        # user.points -= int(jsonObject['usePoints'])
        user.save()

        if int(jsonObject['usePoints']):
            user.subtract_points(int(jsonObject['usePoints']), '사용')
        if real_point:
            user.add_points(real_point, '구매')

    request.session['payment'] = {
        'order_id': order_id,
        'total_amount': order.total_amount
    }
    return JsonResponse({'result': 'success',})


def show_approval(request):
    payment = request.session.get('payment')
    if not payment:
        return HttpResponseNotFound('결제 데이터를 찾을 수 없습니다.')

    order_id = payment.get('order_id')
    total_amount = payment.get('total_amount')


    order = Order.objects.get(pk=order_id)
    context = {
        'order': order,
        'order_id': order_id,
        'total_amount': total_amount,
    }

    del request.session['payment']

    return render(request, 'payments/approval.html', context)