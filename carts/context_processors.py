from .models import Cart

def cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        cart_count = user_cart.cartitems.count()
    context = {
        'cart_count': cart_count,
    }
    return context
