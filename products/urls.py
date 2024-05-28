from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    path('', product_list, name='product_list'),
    path('products/', products, name='products'),
    path('products/<int:pk>', products_detail, name='products'),
    path('add/', product_add, name='product_add'),
    path('edit/<int:pk>/', product_edit, name='product_edit'),
    path('delete/<int:pk>/', product_delete, name='product_delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
