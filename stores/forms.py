from django import forms
from .models import Store, Product, ProductImage, ProductReview
from ckeditor_uploader.fields import RichTextUploadingField

from django.conf import settings

class StoreForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '상점 이름을 입력해 주세요',
                'class': 'form-control',
            },
        )
    )

    content = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '상점을 설명해 주세요',
                'class': 'form-control',
            },
        )
    )
    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-image', 
            }
        ),
        required=True,
    )
    main_image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-image', 
            }
        ),
        required=True,
    )    

    class Meta:
        model = Store
        fields = ('name','image','content', 'main_image')


class ProductForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '상품명을 입력해 주세요',
                'class': 'form-control',
            }
        )
    )
    price = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'placeholder': '가격을 입력해 주세요',
                'class': 'form-control',
            }
        )
    )
    category = forms.CharField(
        widget=forms.Select(
            attrs={
                'class': 'select-control',
            },
        choices=[('미용', '미용'), ('의류', '의류'), ('잡화', '잡화'), ('기타', '기타')],
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
    detail_image = forms.ImageField(
        label = '상품 상세 이미지',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-image', 
            }
        ),
        required=False,
    )

    class Meta:
        model = Product
        fields = ('name', 'price', 'category', 'content','detail_image')


class ProductImageForm(forms.ModelForm):
    image = forms.ImageField(
        label = '상품 이미지',
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True,
                'class': 'form-image', 
            }
        ),
        required=False,
    )

    class Meta:
        model = ProductImage
        fields = ('image',)


class ProductReviewForm(forms.ModelForm):
    title = forms.CharField(
        label = '제목',
        widget=forms.TextInput(
            attrs={
                'placeholder': '제목을 입력해 주세요',
                'class': 'form-control',
            },
        ),
        required=True,
    )
    content = forms.CharField(
        label = False,
        widget = forms.Textarea(
            attrs = {
                'placeholder': '내용을 입력해 주세요',
                'class': 'form-control',
            }
        ),
        required=True,
    )
    rating = forms.IntegerField(
        label = False,
        widget=forms.NumberInput(
            attrs = {
                'placeholder': '평가 점수',
            }
        )
    )

    class Meta:
        model = ProductReview
        fields = ('title', 'content', 'rating', 'image1', 'image2', 'image3', 'image4', 'image5',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['image1', 'image2', 'image3', 'image4', 'image5']:
            self.fields[field_name].widget.attrs.update({'class': 'form-image'})
            self.fields[field_name].label = field_name


