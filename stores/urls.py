from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:store_pk>/', views.detail, name='detail'),
    path('<int:store_pk>/update/', views.update, name='update'),
    path('<int:store_pk>/delete/', views.delete, name='delete'),
    path('<int:store_pk>/create/', views.products_create, name='products_create'),
    path('<int:store_pk>/<int:product_pk>/', views.products_detail, name='products_detail'),
    path('<int:store_pk>/<int:product_pk>/update/', views.products_update, name='products_update'),
    path('<int:store_pk>/<int:product_pk>/delete/', views.products_delete, name='products_delete'),
    path('<int:store_pk>/<int:product_pk>/likes/', views.products_likes, name='products_likes'),
    path('<int:store_pk>/<int:product_pk>/create/', views.reviews_create, name='reviews_create'),
    path('<int:store_pk>/<int:product_pk>/<int:review_pk>/update/', views.reviews_update, name='reviews_update'),
    path('<int:store_pk>/<int:product_pk>/<int:review_pk>/delete/', views.reviews_delete, name='reviews_delete'),
    path('<int:store_pk>/<int:product_pk>/<int:review_pk>/likes/', views.reviews_likes, name='reviews_likes'),
    path('<int:store_pk>/<int:product_pk>/<int:review_pk>/dislikes/', views.reviews_dislikes, name='reviews_dislikes'),
    # 카트..
    # 주문(카카오페이, ...)
]
