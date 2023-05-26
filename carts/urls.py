from django.urls import path
from . import views


app_name = 'carts'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add_item/', views.add_item, name='add_item'),
]