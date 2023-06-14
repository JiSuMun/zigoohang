from django.urls import path
from . import views


app_name = 'carts'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add_item/', views.add_item, name='add_item'),
    path('api/products/<int:product_id>/', views.product_info, name='product_info'),
    path('order_page/', views.order_page, name='order_page'),
    path('modify_quantity/', views.modify_quantity, name='modify_quantity'),
    path('remove_item/', views.remove_item, name='remove_item'),
    # path('increase_item/', views.increase_item, name='increase_item'),
    # path('dicrease_item/', views.dicrease_item, name='dicrease_item'),
    # path('kakaopay/', views.kakaopay, name='kakaopay'),
    # path('kakaopay/approval/<int:order_id>/', views.kakaopay_approval, name='kakaopay_approval'),
    # path('kakaopay/cancel/', views.kakaopay_cancel, name='kakaopay_cancel'),
    # path('kakaopay/fail/', views.kakaopay_fail, name='kakaopay_fail'),
    path('payments/approval/', views.approval, name='approval'),
    path('payments/show_approval/', views.show_approval, name='show_approval'),
    # path('payments/approval/', views.approval, name='approval'),
    # path('payments/approval/', views.approval, name='approval'),
]