from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.main, name='main'),
    path('index', views.index, name='index'),
    path('news/', views.news, name='news'),
    path('create/', views.create, name='create'),
    path('<int:post_pk>/update/', views.update, name='update'),
    path('<int:post_pk>/', views.detail, name='detail'),
    path('<int:post_pk>/delete/', views.delete, name='delete'),
    path('<int:post_pk>/likes/', views.likes, name='likes'),
    path('<int:post_pk>/create/', views.review_create, name='review_create'),
    path('<int:post_pk>/<int:review_pk>/update/', views.review_update, name='review_update'),
    path('<int:post_pk>/<int:review_pk>/likes/', views.review_likes, name='review_likes'),
    path('<int:post_pk>/<int:review_pk>/dislikes/', views.review_dislikes, name='review_dislikes'),
    path('import_zero/', views.import_zero, name='import_zero'),
    path('zero_map/', views.zero_map, name='zero_map'),
    path('get_zeros/', views.get_zeros, name='get_zeros'),
]
