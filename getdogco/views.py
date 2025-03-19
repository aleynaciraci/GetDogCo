from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .forms import DogAdoptionPostForm
from .models import DogAdoptionPost, AdoptionComment
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

# Kullanıcının kendi ilanlarını yönetebileceği panel
@login_required(login_url="user:login")
def dashboard(request):
    posts = DogAdoptionPost.objects.filter(owner=request.user)
    context = {"posts": posts}
    return render(request, "dashboard.html", context)

# Yeni köpek sahiplendirme ilanı ekleme
@login_required(login_url="user:login")
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
    comments = post.comments.all()
    return render(request, "post_detail.html", {"post": post, "comments": comments})

# İlan güncelleme
@login_required(login_url="user:login")
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
@login_required(login_url="user:login")
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