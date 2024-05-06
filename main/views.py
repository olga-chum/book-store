from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now

from goods.models import Categories, Products


def index(request):
    categories = Categories.objects.all()
    manga = Products.objects.filter(category__slug='Manga').order_by('?')[:6]
    new = Products.objects.filter(year_of_publish=datetime.now().year).order_by('?')[:6]

    context: dict = {
        'title': 'Chapter & Verse - Главная',
        'categories': categories,
        'manga': manga,
        'new': new
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