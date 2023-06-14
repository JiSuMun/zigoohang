from django.urls import path
from . import views

app_name = 'challenges'

urlpatterns = [
path('', views.index, name='index'),
path('create/', views.create, name='create'),
path('<int:challenge_pk>/', views.detail, name='detail'),
path('<int:challenge_pk>/update/', views.update, name='update'),
path('<int:challenge_pk>/delete/', views.delete, name='delete'),
path('<int:challenge_pk>/create/', views.certification_create, name='certification_create'),
path('<int:challenge_pk>/<int:certification_pk>/update/', views.certification_update, name='certification_update'),
path('<int:challenge_pk>/<int:certification_pk>/delete/', views.certification_delete, name='certification_delete'),
path('<int:challenge_pk>/participation/', views.participation, name='participation'),
path('<int:challenge_pk>/join/', views.join_challenge, name='join'),
path('<int:challenge_pk>/leave/', views.leave_challenge, name='leave'),
]