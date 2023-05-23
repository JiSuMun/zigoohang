from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from datetime import datetime, timedelta
from django.db.models import Sum
import os
from ckeditor_uploader.fields import RichTextUploadingField


class S_Product(models.Model):
    product = models.CharField(max_length=255)
    price = models.IntegerField()
    content = RichTextUploadingField(blank=True, null=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_s_products', blank=True)
    city = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    extra_address = models.CharField(max_length=100)
    CATEGORY_CHOICES = [('잡화', '잡화'), ('전자제품', '전자제품'), ('의류', '의류'), ('도서', '도서'), ('기타', '기타')]
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)


class S_Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(S_Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


    # 6개월간의 구매내역만 저장
    @staticmethod
    def cleanup_old_purchases():
        six_months_ago = datetime.now() - timedelta(days=180)
        S_Purchase.objects.filter(date__lt=six_months_ago).delete()
    
    # 월별 구매금액
    @classmethod
    def get_monthly_purchase_amount(cls, year, month):
        monthly_purchase = cls.objects.filter(date__year=year, date__month=month).values('user').annotate(total_purchase=Sum('amount'))
        return monthly_purchase


class S_Sales(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(S_Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    # 일별 판매금액
    @classmethod
    def get_total_sales_per_day(cls, date):
        total_sales = cls.objects.filter(date__date=date).aggregate(total_sales=Sum('amount'))
        return total_sales['total_sales'] or 0

    # 월별 판매금액
    @classmethod
    def get_total_sales_per_month(cls, year, month):
        total_sales = cls.objects.filter(date__year=year, date__month=month).aggregate(total_sales=Sum('amount'))
        return total_sales['total_sales'] or 0