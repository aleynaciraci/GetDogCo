from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User 
from PIL import Image, ExifTags # Pillow kütüphanesini kullanarak resim işleme yapabilmek için gerekli

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
    
# Favorilere Ekleme Modeli
class Favorite(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Kullanıcı")
    post = models.ForeignKey("DogAdoptionPost", on_delete=models.CASCADE, verbose_name="İlan")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.post}" # Favoriye ekleyen kullanıcı ve ilan
    
    class Meta:
        unique_together = ('user', 'post') 

# Yorum Modeli
class AdoptionComment(models.Model):
    post = models.ForeignKey(DogAdoptionPost, on_delete=models.CASCADE, verbose_name="İlan", related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Yorum Sahibi", null=True, blank=True)
    comment_author = models.CharField(max_length=50, verbose_name="Yorum Sahibi")
    comment_content = models.TextField(verbose_name="Yorum")
    comment_date = models.DateTimeField(auto_now_add=True, verbose_name="Yorum Tarihi")

    def __str__(self):
        return f"{self.comment_author}: {self.comment_content[:30]}..."

    class Meta:
        ordering = ['-comment_date']

# Kullanıcı Profili Modeli 

from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageOps

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics/')

    def __str__(self):
        return f'{self.user.username} Profili'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        try:
            img = Image.open(self.image.path)

            # ✅ EXIF'e göre otomatik döndür
            img = ImageOps.exif_transpose(img)

            # ✅ Boyutu sınırla
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)

            img.save(self.image.path)

        except Exception as e:
            print("Fotoğraf düzenlenemedi:", e)

# Başvuru Modeli 
class Application(models.Model):
    post = models.ForeignKey(DogAdoptionPost, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=255)
    location_info = models.CharField(max_length=255)
    had_pets_before = models.CharField(max_length=10)
    work_hours = models.CharField(max_length=100, blank=True)
    has_allergy = models.CharField(max_length=10, blank=True)
    motivation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('accepted', 'Kabul Edildi'),
        ('rejected', 'Reddedildi'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    is_read = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.full_name} - {self.post.title}"

# Mesajlaşma Modeli 
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username} ({self.sent_at})" 

