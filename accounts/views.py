from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomAutentication, CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from posts.models import Post
from stores.models import Product, Order, OrderItem, Cart
from secondhands.models import S_Purchase, S_Product


def login(request):
    if request.user.is_authenticated:
        return redirect('main')
    if request.method == 'POST':
        form = CustomAutentication(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('main')
    else:
        form = CustomAutentication()
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('main')


def signup(request):
    if request.user.is_authenticated:
        return redirect('main')
    
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.address = request.POST.get('address')
            user.is_active = False  # 이메일 인증 전까지 비활성화
            user.save()

            # 이메일 인증 메시지 작성
            domain = request.get_host()
            mail_subject = '계정 활성화'
            message = render_to_string('accounts/activate_email.html', {
            'user': user,
            'domain': domain,
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })

            # 이메일 발송
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return render(request, 'accounts/wait_for_email.html')


    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        
        user.save()
        messages.success(request, '가입이 성공적으로 완료되었습니다!')
        return redirect('main')
    else:
        messages.error(request, '이메일 인증 링크가 잘못되었습니다.')
        return HttpResponse('활성화 링크가 유효하지 않습니다.')
    

def user_is_authenticated(user):
    return user.is_authenticated and user.is_active


@user_passes_test(user_is_authenticated, login_url='/accounts/login/')
def main(request):
    return render(request, 'main.html')


@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('main')


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.address = request.POST.get('address')
            form.save()
            return redirect('main')
    else:
        form = CustomUserChangeForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('main')
    else:
        form = CustomPasswordChangeForm(request.user)

    context = {
        'form':form,
    }
    return render(request, 'accounts/change_password.html', context)


@login_required
def profile(request, username):
    q = request.GET.get('q')
    User = get_user_model()
    person = User.objects.get(username=username)
    posts = Post.objects.filter(user=person)
    interests = person.like_products.all()
    orders = Order.objects.filter(customer=person)
    carts = Cart.objects.filter(user=person)
    purchases = S_Purchase.objects.filter(user=person).select_related('product')
    purchase_details = []
    for order in orders:
        items = OrderItem.objects.filter(order=order)
        purchase_details.append({
            'order': order,
            'items': items 
        })
    context = {
        'q':q,
        'person':person,
        'posts':posts,
        'interests':interests,
        'purchase_details': purchase_details,
        'purchases': purchases,
        'carts': carts,
    }
    return render(request, 'accounts/profile.html', context)