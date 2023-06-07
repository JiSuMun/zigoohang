# Generated by Django 3.2.18 on 2023-05-31 06:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_auto_20230531_1557'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('shipping_status', models.CharField(choices=[(0, '결제전'), (1, '배송준비중'), (2, '배송중'), (3, '배송완료'), (4, '취소됨'), (5, '반송중')], max_length=15)),
                ('tracking_number', models.CharField(blank=True, max_length=20, null=True)),
                ('added_at', models.DateField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders_as_customer', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders_as_seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='carts.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.product')),
            ],
        ),
    ]