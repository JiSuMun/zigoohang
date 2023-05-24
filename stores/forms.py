from django import forms
from .models import Store, Product, ProductImage, ProductReview
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
        label = '상품 이미지(필수)',
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True,
            }
        ),
        required=True,
    )

    class Meta:
        model = ProductImage
        fields = ('image',)