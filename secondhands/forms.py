from .models import S_Product, S_ProductImage
from django import forms
from django.conf import settings
import os
from django.forms.widgets import ClearableFileInput


class S_ProductForm(forms.ModelForm):
    product = forms.CharField(
        label='상품명',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': '상품명',
            }
        )
    )
    price = forms.IntegerField(
        label='가격',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control', 
                'placeholder': '가격',
            }
        )
    )
    category = forms.ChoiceField(
        choices=S_Product.CATEGORY_CHOICES, 
        label='카테고리', 
        widget=forms.Select(
            attrs={
                'class': 'form-control', 
                'required': True,
            }
        )
    )
    extra_address = forms.CharField(
    max_length=100, 
    label=False,
    required=False,
    widget=forms.TextInput(
        attrs={
            'placeholder': '상세주소',
            'class': 'form-control', 
            }
        )
    )

    class Meta:
        model = S_Product
        fields = ('product', 'price', 'category', 'content', 'extra_address',)


class CustomClearableFileInput(ClearableFileInput):
    template_name = 'secondhands/custom_clearable_file_input.html'

class S_ProductImageForm(forms.ModelForm):
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
        model = S_ProductImage
        fields = ('image',)


class S_DeleteImageForm(forms.Form):
    delete_images = forms.MultipleChoiceField(
        label='삭제할 이미지 선택',
        required = False,
        widget=forms.CheckboxSelectMultiple,
        choices=[]
    )

    def __init__(self, product, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete_images'].choices = [
            (image.pk, image.image.name) for image in S_ProductImage.objects.filter(product=product)
        ]

    def clean(self):
        cleaned_data = super().clean()
        delete_ids = cleaned_data.get('delete_images')
        if delete_ids:
            images = S_ProductImage.objects.filter(pk__in=delete_ids)
            for image in images:
                os.remove(os.path.join(settings.MEDIA_ROOT, image.image.path))
            images.delete()