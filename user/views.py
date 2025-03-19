from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

# Kullanıcı Kaydı
def register(request):
    form = RegisterForm(request.POST or None)
    
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        newUser = User(username=username)
        newUser.set_password(password)
        newUser.save()

        login(request, newUser)
        messages.success(request, "Başarıyla kayıt oldunuz! Artık ilan ekleyebilirsiniz.")

        return redirect("index")

    context = {
        "form": form
    }
    return render(request, "register.html", context)

# Kullanıcı Girişi
def loginUser(request):
    form = LoginForm(request.POST or None)

    context = {
        "form": form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.warning(request, "Kullanıcı adı veya parola hatalı.")
            return render(request, "login.html", context)

        messages.success(request, "Başarıyla giriş yaptınız! Hoş geldiniz.")
        login(request, user)
        return redirect("index")

    return render(request, "login.html", context)

# Kullanıcı Çıkışı
def logoutUser(request):
    logout(request)
    messages.success(request, "Başarıyla çıkış yaptınız. Tekrar görüşmek üzere!")
    return redirect("index")
