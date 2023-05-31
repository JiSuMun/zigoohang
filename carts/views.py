from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order, OrderItem
from stores.models import Product
from django.http import JsonResponse
import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()
KAKAO_AK = os.getenv('KAKAO_AK')


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
    URL = 'https://kapi.kakao.com/v1/payment/ready'
    headers = {
        'Authorization': 'KakaoAK ' + KAKAO_AK,
    }
    params = {
        'cid': 'TC0ONETIME',    # 테스트용 코드
        'partner_order_id': '1001',     # 주문번호
        'partner_user_id': 'user', # 유저 아이디
        'item_name': 'item',        # 구매 물품 이름
        'quantity': '12',                # 구매 물품 수량
        'total_amount': '12300',        # 구매 물품 가격
        'tax_free_amount': '0',         # 구매 물품 비과세
        'approval_url': f'http://{domain}/carts/kakaopay/approval/', # 결제 승인시 이동할 url
        'cancel_url': f'http://{domain}/carts/kakaopay/cancel/', # 결제 취소 시 이동할 url
        'fail_url': f'http://{domain}/carts/kakaopay/fail/', # 결제 실패 시 이동할 url
    }

    res = requests.post(URL, headers=headers, params=params)
    request.session['tid'] = res.json()['tid']      # 결제 승인시 사용할 tid를 세션에 저장
    next_url = res.json()['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장
    return redirect(next_url)
    # return render(request, 'payments/kakaopay.html', context)


def kakaopay_approval(request):
    context = {
    }
    return render(request, 'payments/kakaopay_approval.html', context)


def kakaopay_cancel(request):
    context = {
    }
    return render(request, 'payments/kakaopay_cancel.html', context)


def kakaopay_fail(request):
    context = {
    }
    return render(request, 'payments/kakaopay_fail.html', context)