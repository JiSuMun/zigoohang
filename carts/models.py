from django.db import models
from django.conf import settings
from stores.models import Product


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"{self.user.username}'의 장바구니"

    def total(self):
        total = 0
        for item in self.cartitems.all():
            total += item.sub_total()
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def sub_total(self):
        return self.product.price * self.quantity