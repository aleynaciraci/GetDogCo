from django.contrib import admin
from django.contrib.auth.models import User 
from .models import DogAdoptionPost, AdoptionComment, ContactMessage, Favorite, Application, Conversation, Message  # Models'dan ilgili sınıfları import ettim

# Başvuru modelini admin paneline kaydetme 
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('post', 'full_name', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('full_name', 'post__title', 'applicant__username')


# Yorumları admin paneline kaydetme
admin.site.register(AdoptionComment)

# İletişim mesajlarını admin paneline kaydetme
admin.site.register(ContactMessage)

# Kullanıcı profili için admin paneli kaydı
from .models import Profile
admin.site.register(Profile)
from django.contrib.auth.models import User 
 
# Favorilere Ekleme Modeli
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__title')  # post modelinde 'title' varsa

# Köpek İlanları İçin Özelleştirilmiş Admin Paneli
@admin.register(DogAdoptionPost)
class DogAdoptionPostAdmin(admin.ModelAdmin):

    list_display = ["title", "owner", "breed", "age", "location", "created_date"]  # Liste görünümü için alanlar
    list_display_links = ["title", "created_date"]  # Tıklanabilir alanlar
    search_fields = ["title", "breed", "location"]  # Arama yapılabilecek alanlar
    list_filter = ["created_date", "breed", "location"]  # Filtreleme için kullanılacak alanlar

    class Meta:
        model = DogAdoptionPost


admin.site.register(Conversation)
admin.site.register(Message)
