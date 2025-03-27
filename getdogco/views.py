from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .forms import DogAdoptionPostForm, ContactForm 
from .models import DogAdoptionPost, AdoptionComment, Favorite 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Tüm köpek sahiplendirme ilanlarını listeleme
def listPosts(request):
    keyword = request.GET.get("keyword")
    if keyword:
        posts = DogAdoptionPost.objects.filter(title__icontains=keyword)
        return render(request, "list_posts.html", {"posts": posts})
    posts = DogAdoptionPost.objects.all()
    return render(request, "list_posts.html", {"posts": posts})

# Ana sayfa
def index(request):
    return render(request, "index.html")

# Hakkımızda sayfası
def about(request):
    return render(request, "about.html")

# İletişim sayfası
def contact_view(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Mesajınız başarıyla gönderildi!")
        return redirect("getdogco:contact")
    
    return render(request, 'contact.html', {"form": form})

# Kullanıcı kayıt işlemi
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hesap oluşturuldu! {username} olarak giriş yapabilirsiniz.')
            return redirect('/user/login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Kullanıcı giriş işlemi
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Hoş geldiniz, {username}!')
                return redirect('/dashboard/')
            else:
                messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Kullanıcı çıkış işlemi
def logout_view(request):
    logout(request)
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('/user/login/')

# Favorilere ekleme ve çıkarma
@login_required
def add_favorite(request, post_id):
    post = get_object_or_404(DogAdoptionPost, id=post_id)
    Favorite.objects.get_or_create(user=request.user, post=post)
    return redirect('post_detail', id=post.id)

@login_required
def remove_favorite(request, post_id):
    post = get_object_or_404(DogAdoptionPost, id=post_id)
    Favorite.objects.filter(user=request.user, post=post).delete()
    return redirect('post_detail', id=post.id)

@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('post')
    return render(request, 'favorites.html', {'favorites': favorites})

def post_detail(request, post_id):
    post = get_object_or_404(DogAdoptionPost, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

# Kullanıcının kendi ilanlarını yönetebileceği panel
@login_required(login_url="getdogco:login")
def dashboard(request):
    posts = DogAdoptionPost.objects.filter(owner=request.user)
    context = {"posts": posts}
    return render(request, "dashboard.html", context)

# Yeni köpek sahiplendirme ilanı ekleme
@login_required(login_url="getdogco:login")
def addDogAdoptionPost(request):
    form = DogAdoptionPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.owner = request.user
        post.save()
        messages.success(request, "İlan başarıyla oluşturuldu")
        return redirect("getdogco:dashboard")
    return render(request, "add_post.html", {"form": form})

# İlan detay sayfası
def postDetail(request, id):
    post = get_object_or_404(DogAdoptionPost, id=id)
    comments = AdoptionComment.objects.filter(post=post)

    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, post=post).exists()

    return render(request, "post_detail.html", {
        "post": post,
        "comments": comments,
        "is_favorited": is_favorited
    })

# İlan güncelleme
@login_required(login_url="getdogco:login")
def updatePost(request, id):
    post = get_object_or_404(DogAdoptionPost, id=id)
    form = DogAdoptionPostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.owner = request.user
        post.save()
        messages.success(request, "İlan başarıyla güncellendi")
        return redirect("getdogco:dashboard")
    return render(request, "update_post.html", {"form": form})

# İlan silme
@login_required(login_url="getdogco:login")
def deletePost(request, id):
    post = get_object_or_404(DogAdoptionPost, id=id)
    post.delete()
    messages.success(request, "İlan başarıyla silindi")
    return redirect("getdogco:dashboard")

# Yoruma ekleme fonksiyonu
def addComment(request, id):
    post = get_object_or_404(DogAdoptionPost, id=id)
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")
        newComment = AdoptionComment(comment_author=comment_author, comment_content=comment_content)
        newComment.post = post
        newComment.save()
    return redirect(reverse("getdogco:post_detail", kwargs={"id": id}))