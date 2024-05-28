""" Forms """
from django import forms
from .models import Product, Category

class CategoryForm(forms.ModelForm):
    """ Category form """
    class Meta:
        model = Category
        fields = ['name', 'visible']


class ProductForm(forms.ModelForm):
    """ Product form """
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'category', 'image', 'visible']