from django.urls import path
from . import views


app_name = 'carts'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    # path('guest/', views.cart_detail_guest, name='cart_detail_guest'),
    path('add_item/', views.add_item, name='add_item'),
]