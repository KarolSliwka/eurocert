from django.http import JsonResponse
from rest_framework import viewsets
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm, CategoryForm


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']
    pagination_class = PageNumberPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


@api_view(["GET", "POST"])
def products(request, format=None):

    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, satus=status.HTTP_201_CREATED)

    return JsonResponse({"products": serializer.data}, safe=False)


@api_view(["GET", "PUT", "DELETE"])
def products_detail(request, pk, format=None):

    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status == status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        product.delete()
        return Response(status == status.HTTP_204_NO_CONTENT)


# Products
def product_list(request):
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(
            category_id=category_id).filter(visible=True)
    else:
        products = Product.objects.all().filter(visible=True)
    categories = Category.objects.all()

    template = 'products/product_list.html'
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id
    }

    return render(request, template, context)


def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()

    template = 'products/product_form.html'
    context = {
        'form': form,
        'form_title': 'Add New Product'
    }

    return render(request, template, context)


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    template = 'products/product_form.html'
    context = {
        'form': form,
        'form_title': 'Edit Product'
    }

    return render(request, template, context)


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('product_list')

    template = 'products/product_confirm_delete.html'
    context = {
        'product': product
    }

    return render(request, template, context)


# Categories
def categories_list(request):
    categories = Category.objects.all()

    template = 'categories/categories_list.html'
    context = {
        'categories': categories,
    }

    return render(request, template, context)


def category_add(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories_list')
    else:
        form = CategoryForm()

    template = 'categories/category_form.html'
    context = {
        'form': form,
        'form_title': 'Add New Category'
    }

    return render(request, template, context)


def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories_list')
    else:
        form = CategoryForm(instance=category)

    template = 'categories/category_form.html'
    context = {
        'form': form,
        'form_title': 'Edit Category'
    }

    return render(request, template, context)


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect('categories_list')

    template = 'categories/category_confirm_delete.html'
    context = {
        'category': category
    }

    return render(request, template, context)
