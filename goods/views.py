from django.shortcuts import render

def catalog(request):
    return render(request, 'goods/catalog.html')

def classica(request):
    return render(request, 'goods/classica.html')

def product(request):
    return render(request, 'goods/product.html')