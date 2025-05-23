from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from getdogco import views
from django.views.i18n import set_language 

urlpatterns = [
    # Set language URL (dil değişimi için)
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns = [
    path('set-language/', set_language, name='set_language'),  # ✅ Dil değişimi için
] 

# i18n_patterns ile çok dilli yapılandırılmış URL’ler
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('getdogco.urls', namespace='getdogco')),
) 

    # Kullanıcı işlemleri
urlpatterns += [
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
        path('profil/', views.profile_view, name='profile'),
        path('sifre-degistir/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
        path('sifre-degistir/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
        path('ilanlar/', views.listPosts, name='list_posts'),
        path('basvur/<int:post_id>/', views.apply_to_post, name='apply_to_post'),
        path("basvurularim/", views.my_post_applications, name="my_applications"),
        path("basvurularim/yaptiklarim/", views.my_send_applications, name="my_send_applications"),
        path("basvuru/<int:app_id>/guncelle/", views.update_application_status, name="update_application_status"),

        path('mesajlasma/', views.conversation_list, name='conversation_list'),
        path('mesajlasma/<int:conversation_id>/', views.messages_with_conversation, name='messages_with_conversation'),
        path('mesajlasma/baslat/<int:user_id>/', views.start_conversation, name='start_conversation'),
        
        path('bildirim/<int:notification_id>/okundu/', views.mark_notification_read, name='mark_notification_read'),
        path('bildirimler/', views.all_notifications, name='all_notifications'),  

        # App urls
        path('', include('getdogco.urls', namespace='getdogco')),
    ]
    
    # /tr/ yazılmasın istiyorsan bunu tut
prefix_default_language = False

# Statik ve medya dosyaları
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
