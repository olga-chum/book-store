from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Categories


def index(request):

    categories = Categories.objects.all()
    context: dict = {
        'title': 'Chapter & Verse - Главная',
        'categories': categories
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