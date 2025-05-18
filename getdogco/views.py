from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, redirect 
from .forms import DogAdoptionPostForm, ContactForm, ProfileUpdateForm, UserUpdateForm, MessageForm
from .models import DogAdoptionPost, AdoptionComment, Favorite, Application, Message, Notification, Conversation 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse 

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


@login_required
def add_favorite(request, post_id):
    post = get_object_or_404(DogAdoptionPost, id=post_id)
    if post.owner == request.user:
        return redirect('post_detail', id=post.id)

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

# Sahiplendirme rehberi 
def adoption_guide(request):
    return render(request, 'adoption_guide.html')

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

@login_required(login_url="getdogco:login")
def addComment(request, id):
    post = get_object_or_404(DogAdoptionPost, id=id)
    
    # Yalnızca POST isteği geldiğinde yorum ekle
    if request.method == "POST":
        # Oturum açmış kullanıcının kullanıcı adıyla comment_author'ı ayarla
        comment_author = request.user.username  # Oturum açmış kullanıcının kullanıcı adı
        comment_content = request.POST.get("comment_content")
        
        # Yeni yorum nesnesini oluştur
        newComment = AdoptionComment(
            comment_author=comment_author,
            comment_content=comment_content
        )
        newComment.post = post  # Yorumun hangi post'a ait olduğunu belirt
        newComment.save()  # Yorum kaydedilsin
    
    # Yorum ekledikten sonra, ilgili post sayfasına yönlendir
    return redirect(reverse("getdogco:post_detail", kwargs={"id": id}))

# Kullanıcı profilini güncelleme 
@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('getdogco:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    user_posts = DogAdoptionPost.objects.filter(owner=request.user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'post_count': user_posts.count(),
    }

    return render(request, 'profile.html', context) 

# Başvuru yapma fonksiyonu 
def apply_to_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(DogAdoptionPost, id=post_id)

        full_name = request.POST.get("full_name")
        contact_info = request.POST.get("contact_info")
        location_info = request.POST.get("location_info")
        had_pets_before = request.POST.get("had_pets_before")
        work_hours = request.POST.get("work_hours")
        has_allergy = request.POST.get("has_allergy")
        motivation = request.POST.get("motivation")

        Application.objects.create(
            post=post,
            applicant=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            contact_info=contact_info,
            location_info=location_info,
            had_pets_before=had_pets_before,
            work_hours=work_hours,
            has_allergy=has_allergy,
            motivation=motivation
        )

        messages.success(request, "Başvurunuz başarıyla iletildi. Teşekkür ederiz!")
        return redirect("getdogco:list_posts")  # İstersen post_detail'e yönlendirebilirsin
    else:
        messages.error(request, "Geçersiz işlem.")
        return redirect("getdogco:list_posts")
    

# Kullanıcının sahip olduğu ilanlara gelen başvurular
@login_required
def my_post_applications(request):
    user_posts = DogAdoptionPost.objects.filter(owner=request.user)
    applications = Application.objects.filter(post__in=user_posts).order_by('-created_at')
    return render(request, "getdogco/my_applications.html", {"applications": applications})

# Başvuru durumu güncelleme (kabul/ret)
@login_required
def update_application_status(request, app_id):
    application = get_object_or_404(Application, id=app_id, post__owner=request.user)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "accept":
            application.status = "accepted"
        elif action == "reject":
            application.status = "rejected"
        application.save()
        messages.success(request, "Başvuru durumu güncellendi.")
    return redirect("getdogco:my_applications")


# 🔁 Sohbet listesi
@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(participants=request.user)
    return render(request, 'messaging/conversation_list.html', {'conversations': conversations})


# 🗨️ Belirli bir sohbet içerisindeki mesajları gösterir ve yeni mesaj gönderimini yapar
@login_required
def messages_with_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    # Eğer kullanıcı bu konuşmanın bir parçası değilse, sohbet listesine yönlendir
    if request.user not in conversation.participants.all():
        return redirect('conversation_list')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.conversation = conversation
            msg.sender = request.user
            msg.save()

            # 🔔 Bildirim oluştur: diğer katılımcıyı bul
            other_user = conversation.participants.exclude(id=request.user.id).first()
            if other_user:
                url = reverse("messages_with_conversation", args=[conversation.id])
                create_notification(
                    user=other_user,
                    message=f"📩 {request.user.username} size yeni bir mesaj gönderdi!",
                    url=url
                )

            # Sayfayı yenilemek için redirect et
            return redirect('messages_with_conversation', conversation_id=conversation.id)
    else:
        form = MessageForm()

    # Mesajları zamana göre sırala (eski → yeni)
    messages = conversation.messages.order_by('timestamp')

    return render(request, 'messaging/messages.html', {
        'conversation': conversation,
        'messages': messages,
        'form': form
    })


# ✉️ Yeni bir konuşma başlat (ya da var olanı bul)
@login_required
def start_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # Bu iki kişi arasında daha önce konuşma var mı?
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()

    # Yoksa oluştur
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

    return redirect('messages_with_conversation', conversation_id=conversation.id) 

def get_or_create_conversation(user1, user2):
    conversation = Conversation.objects.filter(participants=user1).filter(participants=user2).first()
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.set([user1, user2])
    return conversation

# Kullanıcının yaptığı başvurular
@login_required
def my_send_applications(request):
    applications = Application.objects.filter(applicant=request.user).order_by('-created_at')
    return render(request, "getdogco/my_send_applications.html", {
        "applications": applications
    })

# Bildirim oluşturma fonksiyonu  
def create_notification(user, message, url=None):
    Notification.objects.create(user=user, message=message, url=url, is_read=False)

# Bildirimleri görüntüleme 
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    next_url = request.GET.get('next', '/')
    return redirect(next_url)

# Tüm bildirimleri görüntüleme 
@login_required
def all_notifications(request):
    notifications = Notification.objects.filter(user=request.user) 
    return render(request, 'notifications/all_notifications.html', {'notifications': notifications})

from getdogco.models import Notification  # ya da notification modelin nerede ise

def index(request):
    context = {}
    if request.user.is_authenticated:
        context['unread_notification_count'] = Notification.objects.filter(user=request.user, is_read=False).count()
    return render(request, "index.html", context) 