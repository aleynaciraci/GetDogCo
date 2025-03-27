from django import forms 
from .models import DogAdoptionPost, ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adınızı girin'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-posta adresinizi girin'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Mesajınızı yazın',
                'rows': 5
            }),
        }

class DogAdoptionPostForm(forms.ModelForm):
    class Meta:
        model = DogAdoptionPost
        fields = ["title", "description", "breed", "age", "location", "dog_image"]
