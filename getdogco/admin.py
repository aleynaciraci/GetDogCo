from django.contrib import admin
from .models import DogAdoptionPost, AdoptionComment

# Yorumları admin paneline kaydetme
admin.site.register(AdoptionComment)

# Köpek İlanları İçin Özelleştirilmiş Admin Paneli
@admin.register(DogAdoptionPost)
class DogAdoptionPostAdmin(admin.ModelAdmin):

    list_display = ["title", "owner", "breed", "age", "location", "created_date"]  # Liste görünümü için alanlar
    list_display_links = ["title", "created_date"]  # Tıklanabilir alanlar
    search_fields = ["title", "breed", "location"]  # Arama yapılabilecek alanlar
    list_filter = ["created_date", "breed", "location"]  # Filtreleme için kullanılacak alanlar

    class Meta:
        model = DogAdoptionPost
