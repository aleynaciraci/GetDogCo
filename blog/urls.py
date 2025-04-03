from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from getdogco import views  # getdogco içindeki views.py dosyasını çağırıyoruz

urlpatterns = [
    # Yönetici paneli
    path('admin/', admin.site.urls),

    # Kullanıcı işlemleri (/user/login, /user/register, /user/logout)
    path('user/register/', views.register_view, name='register'),
    path('user/login/', views.login_view, name='login'),
    path('user/logout/', views.logout_view, name='logout'),

    # Ana sayfa ve diğer sayfalar
    path('', views.index, name='index'),
    path('post/', views.listPosts, name='list_posts'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.addDogAdoptionPost, name='add_post'),
    path('post/<int:id>/', views.postDetail, name='post_detail'),
    path('update/<int:id>/', views.updatePost, name='update_post'),
    path('delete/<int:id>/', views.deletePost, name='delete_post'),
    path('comment/<int:id>/', views.addComment, name='add_comment'),
    path('about/', views.about, name='about'),
    path('profil/', views.profile_view, name='profile'), # Kullanıcı profili sayfası 
    path('sifre-degistir/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
path('sifre-degistir/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('', include('getdogco.urls', namespace='getdogco')),
] 

# Statik ve medya dosyalarını dahil etme
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
