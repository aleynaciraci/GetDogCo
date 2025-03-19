from django import forms
from .models import DogAdoptionPost

class DogAdoptionPostForm(forms.ModelForm):
    class Meta:
        model = DogAdoptionPost
        fields = ["title", "description", "breed", "age", "location", "dog_image"]
