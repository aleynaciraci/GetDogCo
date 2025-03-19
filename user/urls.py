from django.contrib import admin
from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register, name='register'),  # Kullanıcı kaydı
    path('login/', views.loginUser, name='login'),  # Kullanıcı girişi
    path('logout/', views.logoutUser, name='logout'),  # Kullanıcı çıkışı
]
