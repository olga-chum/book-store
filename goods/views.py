from django.shortcuts import render
from django.template import context

from goods.models import Products

def catalog(request, category_slug):

    goods= Products.objects.filter(category__slug=category_slug)

    context = {
        'title': 'Chepter & Verse: Каталог',
        "goods": goods
    }
    return render(request, 'goods/catalog.html', context)

def product(request, product_slug=False, product_id=False):

    if product_id:
        product = Products.objects.get(id=product_id)
    else:
        product = Products.objects.get(slug=product_slug)

    context = {
        'product': product
    }

    return render(request, 'goods/product.html', context=context)