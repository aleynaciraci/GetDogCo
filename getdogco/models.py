from django.db import models
from ckeditor.fields import RichTextField

# Köpek İlanı Modeli
class DogAdoptionPost(models.Model):
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Sahiplenen Kullanıcı")
    title = models.CharField(max_length=100, verbose_name="İlan Başlığı")
    description = RichTextField(verbose_name="Açıklama")
    breed = models.CharField(max_length=50, verbose_name="Köpek Irkı")
    age = models.IntegerField(verbose_name="Köpek Yaşı")
    location = models.CharField(max_length=100, verbose_name="Konum")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    dog_image = models.ImageField(upload_to='dog_images/', blank=True, null=True, verbose_name="Köpek Fotoğrafı")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']

# İletişim Mesajı Modeli
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

# Yorum Modeli
class AdoptionComment(models.Model):
    post = models.ForeignKey(DogAdoptionPost, on_delete=models.CASCADE, verbose_name="İlan", related_name="comments")
    comment_author = models.CharField(max_length=50, verbose_name="Yorum Sahibi")
    comment_content = models.TextField(verbose_name="Yorum")
    comment_date = models.DateTimeField(auto_now_add=True, verbose_name="Yorum Tarihi")

    def __str__(self):
        return f"{self.comment_author}: {self.comment_content[:30]}..."  # İlk 30 karakteri göster

    class Meta:
        ordering = ['-comment_date']
