from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Kullanıcı Adı",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Kullanıcı adınızı girin"})
    )
    password = forms.CharField(
        label="Parola",
        max_length=20,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Parolanızı girin"})
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        label="Kullanıcı Adı",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Kullanıcı adınızı girin"})
    )
    password = forms.CharField(
        max_length=20,
        label="Parola",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Parolanızı belirleyin"})
    )
    confirm = forms.CharField(
        max_length=20,
        label="Parolayı Doğrula",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Parolanızı tekrar girin"})
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar eşleşmiyor!")

        return cleaned_data
