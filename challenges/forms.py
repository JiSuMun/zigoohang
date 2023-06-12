from django import forms
from .models import Challenge, ChallengeImage, Certification
from django.conf import settings
import os
from django.forms.widgets import ClearableFileInput


class ChallengeForm(forms.ModelForm):
    title = forms.CharField(
        label = False,
        widget=forms.TextInput(
            attrs={
                'placeholder':'첼린지명을 입력해 주세요',
                'class': 'form-control',
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': '내용을 입력해 주세요',
                'class': 'form-control text-form',
            }
        )
    )

    start_date = forms.DateField(
        label="시작 날짜",
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        )
    )
    end_date = forms.DateField(
        label="종료 날짜",
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Challenge
        fields = ('title', 'description', 'start_date', 'end_date')


class CustomClearableFileInput(ClearableFileInput):
    template_name = 'challenges/custom_clearable_file_input.html'

class ChallengeImageForm(forms.ModelForm):
    image = forms.ImageField(
        label='이미지',
        widget=CustomClearableFileInput(
            attrs={
                'multiple': True, 
                'class': 'form-control', 
            }
        ),
    )

    class Meta:
        model = ChallengeImage
        fields = ('image',)


class ChallengeImage_DeleteImageForm(forms.Form):
    delete_images = forms.MultipleChoiceField(
        label='삭제할 이미지 선택',
        required = False,
        widget=forms.CheckboxSelectMultiple,
        choices=[]
    )


    def __init__(self, challenge, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete_images'].choices = [
        (image.pk, image.image.name) for image in ChallengeImage.objects.filter(challenge=challenge)
    ]
    def clean(self):
        cleaned_data = super().clean()
        delete_ids = cleaned_data.get('delete_images')
        if delete_ids:
            images = ChallengeImage.objects.filter(pk__in=delete_ids)
            for image in images:
                os.remove(os.path.join(settings.MEDIA_ROOT, image.image.path))
            images.delete()


class CertificationForm(forms.ModelForm):
    title = forms.CharField(
        label = False,
        widget = forms.TextInput(
            attrs = {
                'placeholder':'인증제목',
                'class': 'form-control',
            }
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': '내용을 입력해 주세요',
                'class': 'form-control text-form',
            }
        )
    )
    
    image = forms.ImageField(
    required=False,
    widget=forms.ClearableFileInput(
        attrs={
            'class': 'form-control',
            }
        )
    )
    class Meta:
        model = Certification
        fields = ('title', 'content', 'image',)
