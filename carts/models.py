from django.db import models
from django.conf import settings
from stores.models import Product
from django.db.models import Sum


POINT_PER_PRICE = 0.01


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
    quantity = models.PositiveIntegerField(default=1)

    def sub_total(self):
        return self.product.price * self.quantity
    

class Order(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders_as_seller')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders_as_customer')
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # amount = models.IntegerField()
    # quantity = models.IntegerField()
    address = models.CharField(max_length=100)
    STATUS_CHOICES = (
        (0, '결제전'),
        (1, '배송준비중'),
        (2, '배송중'),
        (3, '배송완료'),
        (4, '취소됨'),
        (5, '반송중'),
    )
    shipping_status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        # default='배송준비중'
    ) # 배송 상태
    tracking_number = models.CharField(max_length=20, blank=True, null=True) # 운송장 번호 # 배송중상태가 되면 값 입력(ex. order.pk)
    
    added_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username}의 주문번호 {self.pk}"

    # 주문 총 금액
    def total(self):
        total = 0
        for item in self.order_items.all():
            total += item.sub_total()
        return total
    
    # 구매를 하게 되면 구매금액의 일정비율이 포인트로 추가
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        points = self.total() * POINT_PER_PRICE
        self.customer.points += points
        self.customer.save()
    
    @classmethod
    def get_total_sales_per_day(cls, seller, date):
        total_sales = cls.objects.filter(seller=seller, added_at__date=date).aggregate(total_sales=Sum('total'))
        return total_sales['total_sales'] or 0

    @classmethod
    def get_total_sales_per_month(cls, seller, year, month):
        total_sales = cls.objects.filter(seller=seller, added_at__year=year, added_at__month=month).aggregate(total_sales=Sum('total'))
        return total_sales['total_sales'] or 0

    @classmethod
    def get_total_purchase_per_month(cls, customer, year, month):
        total_purchase = cls.objects.filter(customer=customer, added_at__year=year, added_at__month=month).aggregate(total_purchase=Sum('total'))
        return total_purchase['total_purchase'] or 0



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # 상품 pk
    quantity = models.IntegerField() # 상품 개수

    # 주문 item별 금액
    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} - {self.quantity}개"


# class SaleList(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     added_at = models.DateField(auto_now_add=True)
#     pass

# class SaleItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE) # 상품 pk
#     quantity = models.IntegerField() # 상품 개수


# 배송상태 관리
# class ShippingStatus(models.Model):
#     STATUS_CHOICES = (
#         ('배송준비중', '배송준비중'),
#         ('배송중', '배송중'),
#         ('배송완료', '배송완료'),
#     )

#     tracking_number = models.CharField(max_length=100)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.tracking_number

# class Shipment(models.Model):
#     tracking_number = models.CharField(max_length=100)
#     sender = models.CharField(max_length=100)
#     recipient = models.CharField(max_length=100)
#     shipping_status = models.ForeignKey(ShippingStatus, on_delete=models.CASCADE)