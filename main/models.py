from django.db import models

class Dog(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='dog_images/')

    def __str__(self):
        return self.name


# Create your models here.
