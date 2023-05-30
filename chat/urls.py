from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('<int:user_id>/', views.start_chat, name='start_chat'),
    path('<str:room_name>/', views.room, name='room'),
    path('<str:room_name>/delete/', views.delete_chat, name='delete_chat'),
]