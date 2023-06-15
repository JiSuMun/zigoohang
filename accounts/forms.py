from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from accounts.models import User


class FindUserIDForm(forms.Form):
    last_name = forms.CharField(
        label = "이름",
        widget = forms.TextInput(attrs = {
            'placeholder': '이름',
            'class':'form-control',
            }
        ),
    )

    email = forms.EmailField(
        label = "이메일",
        widget = forms.EmailInput(attrs = {
            'placeholder': '이메일',
            'class':'form-control',
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("입력한 이메일이 존재하지 않습니다.")
        
class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label='이메일 주소', required=True, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "이메일",}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("입력한 이메일이 존재하지 않습니다.")
        
class CustomAuthentication(AuthenticationForm):
    username = forms.CharField(
        label = False,
        widget = forms.TextInput(attrs = {
            'class':'form-control',
            "placeholder": "아이디",
            "autocomplete": "username off",
            }
        ),
    )
    password = forms.CharField(
        label = False,
        widget = forms.PasswordInput(attrs = {
            'class':'form-control',
            "placeholder": "비밀번호",
            "autocomplete": "current-password",
            }
        ),
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
                'autocomplete': 'off',
            }
        ),
    )

    first_name = forms.CharField(
        label = "닉네임",
        widget = forms.TextInput(
            attrs = {
                "class": "form-control",
                "placeholder": "닉네임",
                'autocomplete': 'off',
            }
        ),
    )

    last_name = forms.CharField(
        label = "이름",
        widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "이름",
                'autocomplete': 'off',
            }
        ),
    )


    password1 = forms.CharField(
        label = "비밀번호",
        widget = forms.PasswordInput(
            attrs = {
                "class": "form-control",
                "placeholder": "비밀번호 8자리 이상 입력해 주세요",
                'autocomplete': 'new-password',
            }
        ),
    )
    password2 = forms.CharField(
        label = "비밀번호 확인",
        widget = forms.PasswordInput(
            attrs = {
                "class": "form-control",
                "placeholder": "비밀번호 확인",
                'autocomplete': 'off',
            }
        ),
    )


    email = forms.EmailField(
        label = "이메일",
        widget = forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "이메일",
                'autocomplete': 'off',
            }
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'image', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].widget.attrs['class'] = 'form-control form-image'

        
    # is_seller = forms.BooleanField(
    #     required=False,
    #     label="판매자",
    #     widget=forms.CheckboxInput(
    #         attrs={
    #             "type":"checkbox",
    #             "class": "form-check-input",
    #         }
    #     ),
    # )

class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(
        label = "닉네임",
        widget = forms.TextInput(
            attrs = {
                "class": "form-control",
                "placeholder": "닉네임",
            }
        ),
    )

    last_name = forms.CharField(
        label = "이름",
        widget = forms.TextInput(
            attrs = {
                "class": "form-control",
                "placeholder": "홍길동",
            }
        ),
    )

    password = None
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name', 'image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].widget.attrs['class'] = 'form-control form-image'


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
