from django.shortcuts import render, redirect



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
