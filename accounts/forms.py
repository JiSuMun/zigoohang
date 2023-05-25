from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from accounts.models import User

class CustomAutentication(AuthenticationForm):
    username = forms.CharField(
        label = False,
        widget = forms.TextInput(attrs = {
            'class':'form-control',
            "placeholder": "아이디",
            "autocomplete": "username",
            }),
    )
    password = forms.CharField(
        label = False,
        widget = forms.PasswordInput(attrs = {
            'class':'form-control',
            "placeholder": "비밀번호",
            "autocomplete": "current-password",
            }),
    )

    class Meta:
        model = get_user_model
        fields = ('username', 'password')


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label = "아이디",
        widget = forms.TextInput(
            attrs = {
                "class": "form-control",
                "placeholder": "아이디",
            }),
    )

    first_name = forms.CharField(
        label = "닉네임",
        widget = forms.TextInput(
            attrs = {
                "class": "form-control",
                "placeholder": "닉네임",
            }),
    )

    last_name = forms.CharField(
        label = "이름",
        widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "홍길동",
            }),
    )


    password1 = forms.CharField(
        label = "비밀번호",
        widget = forms.PasswordInput(
            attrs = {
                "class": "form-control",
                "placeholder": "******",
            }),
    )
    password2 = forms.CharField(
        label = "비밀번호 확인",
        widget = forms.PasswordInput(
            attrs = {
                "class": "form-control",
                "placeholder": "******",
            }),
    )

    is_seller = forms.BooleanField(
        required=False,
        label="판매자",
        widget=forms.CheckboxInput(
            attrs={
                "type":"checkbox",
                "class": "form-check-input",
            }
        ),
    )

    email = forms.EmailField(
        label = "이메일",
        widget = forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "이메일",
            }),
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'image', 'is_seller', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].widget.attrs['class'] = 'form-control'

class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(
        label = "닉네임",
        widget = forms.TextInput(
            attrs = {
                "class": "form-control",
                "placeholder": "닉네임",
            }),
    )

    last_name = forms.CharField(
        label = "이름",
        widget = forms.TextInput(
            attrs = {
                "class": "form-control",
                "placeholder": "홍길동",
            }),
    )

    password = None
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name', 'image', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].widget.attrs['class'] = 'form-control'


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label = '기존 비밀번호',
        widget = forms.PasswordInput(
            attrs = {
                "class": "form-control",
                "placeholder": "기존 비밀번호",
            }
        ),
    )
    new_password1 = forms.CharField(
        label = "새 비밀번호",
        widget = forms.PasswordInput(
            attrs = {
                "class": "form-control",
                "placeholder": "새 비밀번호",
            }
        ),
        help_text="",
    )
    new_password2 = forms.CharField(
        label = "새 비밀번호 확인",
        widget = forms.PasswordInput(
            attrs = {
                "class": "form-control",
                "placeholder": "새 비밀번호 확인",
            }
        ),
        help_text = "",
    )