from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now
from carts.models import Cart

from goods.models import Categories, Products


def index(request):
    categories = Categories.objects.all()
    manga = Products.objects.filter(category__slug='Manga').order_by('?')[:6]
    new = Products.objects.filter(year_of_publish=datetime.now().year).order_by('?')[:6]
    if request.user.is_authenticated:
        basket = [item.product_id for item in Cart.objects.filter(user=request.user)]
    else:
        basket = [item.product_id for item in Cart.objects.filter(session_key = request.session.session_key)]
    
    context: dict = {
        'title': 'Chapter & Verse - Главная',
        'categories': categories,
        'manga': manga,
        'new': new,
        'basket': basket,
    }

    return render(request, 'main/index.html', context)

def about(request):
    context: dict = {
        'title': 'Chapter & Verse - О нас'
    }
    return render(request, 'main/about.html', context)

def sales(request):
    context: dict = {
        'title': 'Chapter & Verse - Акции'
    }
    return render(request, 'main/sales.html', context)

def else_(request):
    context: dict = {
        'title': 'Chapter & Verse - Что еще почитать?'
    }
    return render(request, 'main/else.html', context)