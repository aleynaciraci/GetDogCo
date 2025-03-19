from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from getdogco import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),  # Ana sayfa
    path('about/', views.about, name="about"),  # Hakkımızda sayfası
    path('posts/', include("getdogco.urls")),  # Köpek ilanlarını yöneten URL'ler
    path('user/', include("user.urls")),  # Kullanıcı işlemleri
]

# Medya dosyalarının (resim, video) sunulması için gerekli ayar
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
