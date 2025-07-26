from django.urls import path
from . import views


urlpatterns = [

    path('user-login', views.UserLoginView),
    path('user-logout', views.UserLogoutView),
    path('user-register', views.UserRegisterView),
    path('verify-otp', views.UserOTPVerifyView),

]
