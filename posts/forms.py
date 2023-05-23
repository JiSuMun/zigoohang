from django import forms
from .models import Post, Review, PostImage, ReviewImage
from taggit.forms import TagWidget
from django.conf import settings
import os


class PostForm(forms.ModelForm):
    title = forms.CharField(
        label = False,
        widget = forms.TextInput(
            attrs = {
                'placeholder':'글제목',
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Post
        fields = ('title', 'content', 'tags',)
        widgets = {
            'tags': TagWidget(attrs={
                'style' : 'width: 400px;',
                'class': 'form-control',
                'placeholder': "태그는 콤마(,)로 구분해주세요.",
                }),
        }
        labels = {
        'tags': '#해시태그:',
        }
        help_texts = {
            'tags': '',
        }


class PostImageForm(forms.ModelForm):
    image = forms.ImageField(
        label='관련 이미지(필수)',
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True, 
                'class': 'form-control', 
                'style': 'width: 400px;',
            }
        ),
    )

    class Meta:
        model = PostImage
        fields = ('image',)


class DeleteImageForm(forms.Form):
    delete_images = forms.MultipleChoiceField(
        label='삭제할 이미지 선택',
        required = False,
        widget=forms.CheckboxSelectMultiple,
        choices=[]
    )

    def __init__(self, post, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete_images'].choices = [
            (image.pk, image.image.name) for image in PostImage.objects.filter(post=post)
        ]

    def clean(self):
        cleaned_data = super().clean()
        delete_ids = cleaned_data.get('delete_images')
        if delete_ids:
            images = PostImage.objects.filter(pk__in=delete_ids)
            for image in images:
                os.remove(os.path.join(settings.MEDIA_ROOT, image.image.path))
            images.delete()


class ReviewForm(forms.ModelForm):
    title = forms.CharField(
        label = False,
        widget = forms.TextInput(
            attrs = {
                'placeholder':'리뷰제목',
                'class': 'form-control',
            }
        )
    )

    
    class Meta:
        model = Review
        fields = ('title', 'content', )


class ReviewImageForm(forms.ModelForm):
    image = forms.ImageField(
        label='이미지 선택',
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True, 
                'class': 'form-control', 
                'style' : 'width: 400px;'
            }
        ),
    )

    class Meta:
        model = ReviewImage
        fields = ('image',)

    def clean(self):
        cleaned_data = super().clean()
        images = self.files.getlist('image')


class DeleteReviewImageForm(forms.Form):
    delete_images = forms.MultipleChoiceField(
        label='삭제할 이미지 선택',
        required = False,
        widget=forms.CheckboxSelectMultiple,
        choices=[]
    )

    def __init__(self, review, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete_images'].choices = [
            (image.pk, image.image.name) for image in ReviewImage.objects.filter(review=review)
        ]

    def clean(self):
        cleaned_data = super().clean()
        delete_ids = cleaned_data.get('delete_images')
        if delete_ids:
            images = ReviewImage.objects.filter(pk__in=delete_ids)
            for image in images:
                os.remove(os.path.join(settings.MEDIA_ROOT, image.image.path))
            images.delete()