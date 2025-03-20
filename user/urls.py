from django.contrib import admin
from django.urls import path
from . import views

app_name = 'getdogco'

urlpatterns = [
    path('register/', views.register, name='register'),  # Kullanıcı kaydı
    path('login/', views.login_view, name='login'),  # Kullanıcı girişi
    path('logout/', views.logout_view, name='logout'),  # Kullanıcı çıkışı
]
