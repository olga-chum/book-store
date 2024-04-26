from django.shortcuts import render
from django.template import context

from goods.models import Products

def classica(request):

    goods= Products.objects.all()

    context = {
        'title': 'Chepter & Verse: Классика',
        "goods": goods
    }
    return render(request, 'goods/classica.html', context)

def product(request):
    return render(request, 'goods/product.html')