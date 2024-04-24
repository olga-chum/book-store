from django.shortcuts import render
from django.template import context

def catalog(request):
    return render(request, 'goods/catalog.html')

def classica(request):
    context = {
        'title': 'Chepter & Verse: Классика'
    }
    return render(request, 'goods/classica.html', context)

def product(request):
    return render(request, 'goods/product.html')