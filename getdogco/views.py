from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Dog

# Ana sayfa  
def home(request):
    return render(request, 'home.html')

# Kayıt olma (signup)
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('welcome')  # Kayıttan sonra hoş geldin sayfasına yönlendir
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Kullanıcı girişi
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('welcome')  # Girişten sonra hoş geldin sayfasına yönlendir
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Kullanıcı çıkışı
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

# Hoş geldin sayfası (Giriş yapan kullanıcılar için)
@login_required
def welcome(request):
    return render(request, 'welcome.html')

# Kullanıcı profili (Giriş gereklidir)
@login_required
def profile(request):
    return render(request, 'profile.html')

# Şifre sıfırlama sayfası
def forgot_password(request):
    return render(request, 'forgot-password.html')

# Sahiplenilmiş köpeklerin listesi (Giriş yapmış kullanıcılar görebilir)
@login_required
def adopted_dogs(request):
    return render(request, 'adopted.html')

# Tüm köpeklerin listesi
def dog_list(request):
    dogs = Dog.objects.all()  # Veritabanındaki tüm köpekleri al
    return render(request, 'dog-list.html', {'dogs': dogs})

# Köpek detay sayfası
def dog_detail(request, dog_id):
    dog = get_object_or_404(Dog, id=dog_id)
    return render(request, 'dog-detail.html', {'dog': dog})