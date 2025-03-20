from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from getdogco import views

urlpatterns = [
    # Your existing paths
    path('', views.listPosts, name='list_posts'),
    path('about/', views.about, name='about'),
    path('posts/', views.listPosts, name='posts'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.addDogAdoptionPost, name='add_post'),
    path('post/<int:id>/', views.postDetail, name='post_detail'),
    path('update/<int:id>/', views.updatePost, name='update_post'),
    path('delete/<int:id>/', views.deletePost, name='delete_post'),
    path('comment/<int:id>/', views.addComment, name='add_comment'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Medya dosyalarının (resim, video) sunulması için gerekli ayar
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)