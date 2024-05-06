from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render
from django.shortcuts import get_object_or_404
from django.template import context
from datetime import datetime
from goods.models import Products
from goods.models import Categories
from goods.utils import q_search

def catalog(request, category_slug=None):

    query = request.GET.get('q', None)

    if query:
        goods = q_search(query)
        category = None
    else:
        goods= get_list_or_404(Products.objects.filter(category__slug=category_slug))
        category = get_object_or_404(Categories, slug=category_slug)

    context = {
        'title': 'Chepter & Verse: Каталог',
        "goods": goods,
        "slug_url": category_slug,
        "current_category": category
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

def bestsellers(request):
    categories = Categories.objects.all()
    bests = Products.objects.filter(quantity__lt=5).order_by('?')[:6]
    context: dict = {
        'title': 'Chapter & Verse - Бестселлеры',
        'categories': categories,
        'bests': bests,
    }
    return render(request, 'goods/bestsellers.html', context)

def new(request):
    categories = Categories.objects.all()
    new = Products.objects.filter(year_of_publish=datetime.now().year)
    context: dict = {
        'title': 'Chapter & Verse - Новинки',
        'categories': categories,
        'new': new,
    }
    return render(request, 'goods/new.html', context)