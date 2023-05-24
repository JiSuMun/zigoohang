from django import forms
from .models import Store, Product, ProductImage, ProductReview
from ckeditor_uploader.fields import RichTextUploadingField

from django.conf import settings

class StoreForm(forms.ModelForm):
    name = forms.CharField(
        label='상점 이름',
        widget=forms.TextInput(
            attrs={
                'placeholder': '상점 이름',
            },
        )
    )
    image = forms.ImageField(
        label = '대표이미지(필수)',
        widget=forms.FileInput(
            attrs={

            }
        ),
        required=True,
    )

    class Meta:
        model = Store
        fields = ('name','image',)


class ProductForm(forms.ModelForm):
    name = forms.CharField(
        label='상품명',
        widget=forms.TextInput(
            attrs={
                'placeholder': '상품명',
            }
        )
    )
    price = forms.IntegerField(
        label='가격',
        widget=forms.NumberInput(
            attrs={
                'placeholder': '가격',
            }
        )
    )
    category = forms.CharField(
        label = '카테고리',
        widget=forms.Select(
            attrs={

            },
        choices=[('미용', '미용'), ('의류', '의류'), ('잡화', '잡화'), ('기타', '기타')],
        )
    )

    class Meta:
        model = Product
        fields = ('name', 'price', 'category', 'content',)


class ProductImageForm(forms.ModelForm):
    image = forms.ImageField(
        label = '상품 이미지',
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True,
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
                'placeholder': '리뷰 제목',
            },
        ),
        required=True,
    )
    # content = forms.CharField(
    #     label = False,
    #     widget = forms.Textarea(
    #         attrs = {
    #             'placeholder': '리뷰를 입력해주세요.',
    #         }
    #     )
    # )
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
            self.fields[field_name].widget.attrs.update({'class': ''})
            self.fields[field_name].label = field_name


