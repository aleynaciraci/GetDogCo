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
from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static 

app_name = "getdogco"

urlpatterns = [
    path('', views.index, name="index"),
    path('post/', views.listPosts, name='list_posts'),
    path('posts/add/', views.addDogAdoptionPost, name="add_post"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('post/<int:id>/', views.postDetail, name="post_detail"),
    path('update/<int:id>/', views.updatePost, name="update_post"),
    path('delete/<int:id>/', views.deletePost, name="delete_post"),
    path('comment/<int:id>/', views.addComment, name="add_comment"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact_view, name="contact"),
    path('favorites/add/<int:post_id>/', views.add_favorite, name='add_favorite'),
    path('favorites/remove/<int:post_id>/', views.remove_favorite, name='remove_favorite'),
    path('my-favorites/', views.my_favorites, name='my_favorites'),
    path('guide/', views.adoption_guide, name='adoption_guide'),# Sahiplendirme rehberi
    path('profil/', views.profile_view, name='profile'), # Kullanıcı profili 
    path('ilanlar/', views.listPosts, name='list_posts'),
    path('basvur/<int:post_id>/', views.apply_to_post, name='apply_to_post'), # İlan başvuru 
    path("basvurularim/", views.my_post_applications, name="my_applications"),
    path("basvurularim/yaptiklarim/", views.my_send_applications, name="my_send_applications"),
    path("basvuru/<int:app_id>/guncelle/", views.update_application_status, name="update_application_status"),
    path('mesajlar/<int:user_id>/', views.messages_with_user, name='messages_with_user_alt'),
    path("mesajlasma/baslat/<int:user_id>/", views.start_conversation, name="start_conversation"),
    path("mesajlasma/<int:user_id>/", views.messages_with_user, name="messages_with_user"),
    path('bildirim/<int:notification_id>/okundu/', views.mark_notification_read, name='mark_notification_read'),
    path('bildirimler/', views.all_notifications, name='all_notifications'),  # bu adımı aşağıda anlatacağım


    path('user/register/', views.register_view, name="register"),  # Kullanıcı kayıt
    path('user/login/', views.login_view, name="login"),  # Kullanıcı girişi
    path('user/logout/', views.logout_view, name="logout"),  # Kullanıcı çıkışı

]  