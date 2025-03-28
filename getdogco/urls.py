"""
URL configuration for getdogco project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

app_name = "getdogco"  

urlpatterns = [
    path('', views.index, name="index"),  # Anasayfa
    path('post/', views.listPosts, name='list_posts'), # Tüm ilanları listeleme
    path('posts/add/', views.addDogAdoptionPost, name="add_post"),  # Yeni ilan ekleme
    path('dashboard/', views.dashboard, name="dashboard"),  # Kullanıcı paneli
    path('post/<int:id>/', views.postDetail, name="post_detail"),  # İlan detay sayfası
    path('update/<int:id>/', views.updatePost, name="update_post"),  # İlan güncelleme
    path('delete/<int:id>/', views.deletePost, name="delete_post"),  # İlan silme
    path('comment/<int:id>/', views.addComment, name="add_comment"),  # Yorum ekleme
    path('about/', views.about, name="about"),  # Hakkımızda sayfası
    path('contact/', views.contact_view, name="contact"), # İletişim sayfası
    path('favorites/add/<int:post_id>/', views.add_favorite, name='add_favorite'), # Favorilere ekleme
    path('favorites/remove/<int:post_id>/', views.remove_favorite, name='remove_favorite'), # Favorilerden kaldırma
    path('my-favorites/', views.my_favorites, name='my_favorites'), # Favorilerim
    path('guide/', views.adoption_guide, name='adoption_guide'), # Sahiplendirme rehberi
    path('user/register/', views.register_view, name="register"),  # Kullanıcı kayıt
    path('user/login/', views.login_view, name="login"),  # Kullanıcı girişi
    path('user/logout/', views.logout_view, name="logout"),  # Kullanıcı çıkışı
]