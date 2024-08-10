from calendar import c
from django.shortcuts import get_list_or_404, render
from django.shortcuts import get_object_or_404
from datetime import datetime
from goods.models import Products
from goods.models import Categories
from goods.utils import q_search
from carts.models import Cart, Like
from main.forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail

def catalog(request, category_slug=None):
    query = request.GET.get('q', None)
    modal_form, redirect_anchor = handle_contact_form(request)

    if request.user.is_authenticated:
        basket = [item.product_id for item in Cart.objects.filter(user=request.user)]
        favourites = [item.product_id for item in Like.objects.filter(user=request.user)]
    else:
        basket = [item.product_id for item in Cart.objects.filter(session_key = request.session.session_key)]
        favourites = [item.product_id for item in Like.objects.filter(session_key = request.session.session_key)]

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
        "current_category": category,
        'basket': basket,
        'favourites': favourites,
        'modal_form': modal_form,
        'redirect_anchor': redirect_anchor
        
    }
    return render(request, 'goods/catalog.html', context)

def product(request, product_slug=False, product_id=False):
    modal_form, redirect_anchor = handle_contact_form(request)
    if request.user.is_authenticated:
        basket = [item.product_id for item in Cart.objects.filter(user=request.user)]
        favourites = [item.product_id for item in Like.objects.filter(user=request.user)]
    else:
        basket = [item.product_id for item in Cart.objects.filter(session_key = request.session.session_key)]
        favourites = [item.product_id for item in Like.objects.filter(session_key = request.session.session_key)]

    if product_id:
        product = Products.objects.get(id=product_id)
    else:
        product = Products.objects.get(slug=product_slug)

    context = {
        'product': product,
        'basket': basket,
        'favourites': favourites,
        'modal_form': modal_form,
        'redirect_anchor': redirect_anchor   
    }
    return render(request, 'goods/product.html', context=context)

def bestsellers(request):
    categories = Categories.objects.all()
    bests = Products.objects.filter(quantity__lt=5).order_by('?')[:6]
    modal_form, redirect_anchor = handle_contact_form(request)
    if request.user.is_authenticated:
        basket = [item.product_id for item in Cart.objects.filter(user=request.user)]
        favourites = [item.product_id for item in Like.objects.filter(user=request.user)]
    else:
        basket = [item.product_id for item in Cart.objects.filter(session_key = request.session.session_key)]
        favourites = [item.product_id for item in Like.objects.filter(session_key = request.session.session_key)]

    context: dict = {
        'title': 'Chapter & Verse - Бестселлеры',
        'categories': categories,
        'bests': bests,
        'basket': basket,
        'favourites': favourites,
        'modal_form': modal_form,
        'redirect_anchor': redirect_anchor
        
    }
    return render(request, 'goods/bestsellers.html', context)

def new(request):
    categories = Categories.objects.all()
    new = Products.objects.filter(year_of_publish=datetime.now().year)
    modal_form, redirect_anchor = handle_contact_form(request)

    if request.user.is_authenticated:
        basket = [item.product_id for item in Cart.objects.filter(user=request.user)]
        favourites = [item.product_id for item in Like.objects.filter(user=request.user)]
    else:
        basket = [item.product_id for item in Cart.objects.filter(session_key = request.session.session_key)]
        favourites = [item.product_id for item in Like.objects.filter(session_key = request.session.session_key)]

    context: dict = {
        'title': 'Chapter & Verse - Новинки',
        'categories': categories,
        'new': new,
        'basket': basket,
        'favourites': favourites,
        'modal_form': modal_form,
        'redirect_anchor': redirect_anchor
        
    }
    return render(request, 'goods/new.html', context)

def send_contact_email(first_name, username, message):
    subject = "Сообщение с вашего сайта"
    body = f"Сообщение от {first_name} ({username}):\n\n{message}"
    from_email = 'olechka.chumakovachumakova@yandex.ru'  # Адрес электронной почты отправителя
    to_email = 'olechka.chumakovachumakova@yandex.ru'  # Адрес электронной почты, куда придет письмо
    
    send_mail(
        subject,
        body,
        from_email, 
        [to_email], 
        fail_silently=False
    )

def handle_contact_form(request):
    if request.method == 'POST':
        modal_form = ContactForm(request.POST)
        redirect_anchor = '#contacts'
        if modal_form.is_valid():
            fisrt_name = modal_form.cleaned_data['first_name']
            username = modal_form.cleaned_data['username']
            message = modal_form.cleaned_data['message']
            send_contact_email(fisrt_name, username, message)
            messages.success(request, "Сообщение успешно отправлено!")
        else:
            errors = {field: error for field, error in modal_form.errors.items()}
            messages.error(request, "Ошибка при отправке сообщения")
    else:
        modal_form = ContactForm()  # Создаем новую форму для GET-запроса
        redirect_anchor = None
    return modal_form, redirect_anchor