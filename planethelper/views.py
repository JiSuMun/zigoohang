from django.shortcuts import render, redirect
from stores.models import Product
import random

def main(request):
    products = Product.objects.all()
    if len(products) >= 4:
        products = random.sample(list(products),4)
    context = {
        'products': products,
    }
    return render(request, 'main.html', context)