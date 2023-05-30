from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
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
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from posts.models import Post
from stores.models import Product, Order, OrderItem
from secondhands.models import S_Purchase, S_Product
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from .forms import FindUserIDForm, PasswordResetRequestForm
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import SetPasswordForm
from django.views.generic import View

from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from carts.models import Cart, CartItem

import json

class CustomLoginView(LoginView):    
    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'message': 'Username or password is incorrect'})

    def form_valid(self, form):
        # 로그인 작업 완료
        # login(self.request, form.get_user())
        auth_login(self.request, form.get_user())

        cart_data = self.request.POST.get('cart_data')
        if cart_data:
            cart_items = json.loads(cart_data)
            
            # 인증된 사용자를 사용하여 Cart 인스턴스 생성 또는 조회
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            
            # cart_data를 CartItem에 저장, 이미 존재하는 경우 quantity 업데이트
            for item in cart_items:
                # product 인스턴스를 가져옵니다 (id로 조회).
                product_instance = get_object_or_404(Product, id=item['id'])

                # 기존 cart_item이 있는지 확인함
                cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, product=product_instance)

                if cart_item_created:
                    # 새로운 cart_item의 경우
                    cart_item.quantity = item['quantity']
                else:
                    # 기존 cart_item의 경우 quantity를 더해줌
                    cart_item.quantity += item['quantity']

                # 변경된 quantity 값을 저장함
                cart_item.save()

        # 로그인 한 사용자의 프로필로 리디렉션
        # return HttpResponseRedirect(self.get_success_url())
        return JsonResponse({'status': 'success', 'redirect_url': self.get_success_url()})

def login(request):
    if request.user.is_authenticated:
        return redirect('main')
    # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@', request.body)
    if request.method == 'POST':
        # jsonObj = 
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


# class AgreementView(View):
#     def get(self, request, *args, **kwargs):
#         request.session['agreement'] = False
#         return render(request, 'accounts/agreement.html')

#     def post(self, request, *args, **kwarg):
#         if request.POST.get('agreement1', False) and request.POST.get('agreement2', False):
#             request.session['agreement'] = True

#             if request.POST.get('csregister') == 'csregister':       
#                 return redirect('accounts:signup')
#             else:
#                 return redirect('accounts:signup')
#         else:
#             messages.info(request, "약관에 모두 동의해주세요.")
#             return render(request, 'accounts/agreement.html')
        
        
# def signup(request):
#     if request.user.is_authenticated:
#         return redirect('main')
    
#     form = CustomUserCreationForm()
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.address = request.POST.get('address')
#             user.is_active = False  # 이메일 인증 전까지 비활성화
#             user.save()

#             # 이메일 인증 메시지 작성
#             domain = request.get_host()
#             mail_subject = '계정 활성화'
#             message = render_to_string('accounts/activate_email.html', {
#             'user': user,
#             'domain': domain,
#             'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': default_token_generator.make_token(user),
#         })

#             # 이메일 발송
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(mail_subject, message, to=[to_email])
#             email.send()

#             return render(request, 'accounts/wait_for_email.html')

#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/signup.html', context)



class SignupView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main')

        form = CustomUserCreationForm()
        context = {
            'form': form,
        }
        return render(request, 'accounts/signup.html', context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main')
        
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.address = request.POST.get('address')
            user.is_active = False  # Deactivate user until email confirmation
            user.save()

            # Send email activation message
            domain = request.get_host()
            mail_subject = '계정 활성화'
            message = render_to_string('accounts/activate_email.html', {
                'user': user,
                'domain': domain,
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            # Send email
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return JsonResponse({'status': 'success'})

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
        return redirect('accounts:login')
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
    interests = request.user.like_products.all()
    orders = Order.objects.filter(customer=person)
    # purchases = S_Purchase.objects.filter(user=person).select_related('product')
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
        # 'purchases': purchases,
    }
    return render(request, 'accounts/profile.html', context)
    

User = get_user_model()

def find_user_id(request):
    if request.method == 'POST':
        form = FindUserIDForm(request.POST)
        if form.is_valid():
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            users = User.objects.filter(email=email)
            if users:
                for user in users:
                    messages.success(
                        request, f'찾으신 이름: {user.last_name} 이메일: {user.email} 의 사용자명: {user.username}')
                return redirect('accounts:find_user_id')
            else:
                messages.error(request, '입력하신 이메일로 가입된 아이디를 찾을 수 없습니다.')
                return redirect('accounts:find_user_id')
    else:
        form = FindUserIDForm()
    return render(request, 'accounts/find_user_id.html', {'form': form})


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                # 이메일 발송 로직
                subject = "비밀번호 재설정 요청"
                email_template_name = "accounts/password_reset_email.html"
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                default_path = reverse('accounts:password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
                c = {
                    "email": user.email,
                    "domain": request.META['HTTP_HOST'],
                    "site_name": 'your_site_name',
                    "uid": uidb64,
                    "user": user,
                    "token": token,
                    "protocol": 'https',
                    "path": default_path,
                }
                email = render_to_string(email_template_name, c)
                send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                messages.success(request, '비밀번호 재설정 이메일이 발송되었습니다.')
                return redirect('accounts:login')
            else:
                messages.error(request, '입력한 사용자명에 해당하는 계정을 찾을 수 없습니다.')
                return redirect('accounts:password_reset_request')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'accounts/password_reset_request.html', {'form': form})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # 기본 토큰 생성기를 사용한 토큰 검사
    if user is not None and default_token_generator.check_token(user, token):
        form = SetPasswordForm(user, request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, '비밀번호가 변경되었습니다.')
                return redirect('accounts:login')
        return render(request, 'accounts/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, '비밀번호 재설정 링크가 유효하지 않습니다.')
        return redirect('accounts:password_reset_request')