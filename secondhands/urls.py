from django.urls import path
from . import views

app_name = 'secondhands'
urlpatterns = [
    path('index', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:product_pk>/update/', views.update, name='update'),
    path('<int:product_pk>/', views.detail, name='detail'),
    path('<int:product_pk>/delete/', views.delete, name='delete'),
    path('<int:product_pk>/likes/', views.likes, name='likes'),
    # 거래상태 변경
    path('change_status/<int:product_id>/<str:new_status>/', views.change_status, name='change_status'),
]
