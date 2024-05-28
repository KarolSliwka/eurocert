from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    # products api/products/1
    path('products/<int:pk>', products_detail, name='products'),
    path('products/', products, name='products'),

    # products
    path('', product_list, name='product_list'),
    path('add/', product_add, name='product_add'),
    path('edit/<int:pk>/', product_edit, name='product_edit'),
    path('delete/<int:pk>/', product_delete, name='product_delete'),

    # categories
    path('categories/', categories_list, name='categories_list'),
    path('categories/add/', category_add, name='category_add'),
    path('categories/edit/<int:pk>/', category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', category_delete, name='category_delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
