from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView
from .views import SignupView, activate




app_name = "accounts"
urlpatterns = [
    # path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'), 
    path('login/', views.CustomLoginView.as_view(template_name='accounts/login.html'), name='login'),
    path("logout/", views.logout, name="logout"),
    path('signup/', SignupView.as_view(), name='signup'),
    path("update/", views.update, name="update"),
    path('delete/', views.delete, name='delete'),
    path("password/", views.change_password, name="change_password"),
    path("profile/<str:username>/", views.profile, name="profile"),
    # path('agreement/', views.AgreementView.as_view(), name='agreement'),
    # 이메일 인증 
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
    # 아이디/비밀번호 찾기
    path('find_user_id/', views.find_user_id, name='find_user_id'),
    path('password_reset_request/', views.password_reset_request, name='password_reset_request'),
    path('password_reset_confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
]