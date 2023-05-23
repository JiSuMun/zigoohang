from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from datetime import datetime, timedelta
from django.db.models import Sum
import os
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MinValueValidator, MaxValueValidator

POINT_PER_PRICE = 0.01

class Store(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    content = RichTextUploadingField(blank=True, null=True)
    price = models.IntegerField()  # 상품가격
    rating = models.DecimalField(default=0, max_digits=5, decimal_places=1)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_products', blank=True)
    CATEGORY_CHOICES = [('미용', '미용'), ('의류', '의류'), ('잡화', '잡화'), ('기타', '기타')]
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='p_reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = RichTextUploadingField(blank=True,null=True)
    rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_p_reviews')
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislike_p_reviews')


    def save(self, *args, **kwargs):
        self.product.rating = (self.product.rating*self.product.p_reviews.count() + self.rating) / (self.product.p_reviews.count() + 1)
        self.product.save()
        super(ProductReview, self).save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username}'의 장바구니"

    def get_total_price(self):
        return self.product.price * self.quantity


#
class Order(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # amount = models.IntegerField()
    # quantity = models.IntegerField()
    address = models.CharField(max_length=100)
    STATUS_CHOICES = (
        ('배송준비중', '배송준비중'),
        ('배송중', '배송중'),
        ('배송완료', '배송완료'),
        ('취소됨', '취소됨'),
        ('반송중', '반송중'),
    )
    shipping_status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='배송준비중'
    ) # 배송 상태
    tracking_number = models.CharField(max_length=20, blank=True, null=True) # 운송장 번호 # 배송중상태가 되면 값 입력(ex. order.pk)
    
    added_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}의 주문번호 {self.pk}"

    # 주문 총 금액
    def total(self):
        total = 0
        for item in self.order_items.all():
            total += item.sub_total()
        return total
    
    # 구매를 하게 되면 구매금액의 일정비율이 포인트로 추가
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        points = self.quantity * POINT_PER_PRICE
        self.user.points += points
        self.user.save()
    
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
class ShippingStatus(models.Model):
    STATUS_CHOICES = (
        ('배송준비중', '배송준비중'),
        ('배송중', '배송중'),
        ('배송완료', '배송완료'),
    )

    tracking_number = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tracking_number

class Shipment(models.Model):
    tracking_number = models.CharField(max_length=100)
    sender = models.CharField(max_length=100)
    recipient = models.CharField(max_length=100)
    shipping_status = models.ForeignKey(ShippingStatus, on_delete=models.CASCADE)




# class Purchase(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     amount = models.IntegerField()
#     quantity = models.IntegerField()
#     date = models.DateTimeField(auto_now_add=True)

#     # 구매를 하게 되면 거래건수 별 금액이 포인트로 추가
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)

#         # points = int(self.amount * 0.01)
#         points = self.quantity * POINT_PER_PRICE # 변수명 변경해야함
#         self.user.points += points
#         self.user.save()

#     # 6개월간의 구매내역만 저장
#     @staticmethod
#     def cleanup_old_purchases():
#         six_months_ago = datetime.now() - timedelta(days=180)
#         Purchase.objects.filter(date__lt=six_months_ago).delete()
    
#     # 월별 구매금액
#     @classmethod
#     def get_monthly_purchase_amount(cls, year, month):
#         monthly_purchase = cls.objects.filter(date__year=year, date__month=month).values('user').annotate(total_purchase=Sum('amount'))
#         return monthly_purchase


# class Sales(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     date = models.DateTimeField(auto_now_add=True)

#     # 일별 판매금액
#     @classmethod
#     def get_total_sales_per_day(cls, date):
#         total_sales = cls.objects.filter(date__date=date).aggregate(total_sales=Sum('amount'))
#         return total_sales['total_sales'] or 0

#     # 월별 판매금액
#     @classmethod
#     def get_total_sales_per_month(cls, year, month):
#         total_sales = cls.objects.filter(date__year=year, date__month=month).aggregate(total_sales=Sum('amount'))
#         return total_sales['total_sales'] or 0