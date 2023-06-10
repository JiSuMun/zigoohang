from django.urls import path
from . import views

app_name = 'challenges'

urlpatterns = [
path('', views.index, name='index'),
path('create/', views.create, name='create'),
path('<int:challenge_pk>/', views.detail, name='detail'),
path('<int:challenge_pk>/update/', views.update, name='update'),
path('<int:challenge_pk>/delete/', views.delete, name='delete'),
]