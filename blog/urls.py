from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from getdogco import views  # getdogco içindeki views.py dosyasını çağırıyoruz

urlpatterns = [
    # Yönetici paneli
    path('admin/', admin.site.urls),

    # Kullanıcı işlemleri (/user/login, /user/register, /user/logout)
    path('user/register/', views.register_view, name='register'),
    path('user/login/', views.login_view, name='login'),
    path('user/logout/', views.logout_view, name='logout'),

    # Ana sayfa ve diğer sayfalar
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.addDogAdoptionPost, name='add_post'),
    path('post/<int:id>/', views.postDetail, name='post_detail'),
    path('update/<int:id>/', views.updatePost, name='update_post'),
    path('delete/<int:id>/', views.deletePost, name='delete_post'),
    path('', views.listPosts, name='list_posts'),
    path('comment/<int:id>/', views.addComment, name='add_comment'),
    path('about/', views.about, name='about'),
] 

# Statik ve medya dosyalarını dahil etme
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
