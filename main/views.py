from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now
from carts.models import Cart, Like
from django.http import HttpResponseRedirect
from django.urls import reverse

from goods.models import Categories, Products
from main.forms import ContactForm
from django.contrib import messages

from django.core.mail import send_mail


def index(request):
    modal_form, redirect_anchor = handle_contact_form(request)
    categories = Categories.objects.all()
    manga = Products.objects.filter(category__slug='Manga').order_by('?')[:6]
    new = Products.objects.filter(year_of_publish=datetime.now().year).order_by('?')[:6]
    if request.user.is_authenticated:
        basket = [item.product_id for item in Cart.objects.filter(user=request.user)]
        favourites = [item.product_id for item in Like.objects.filter(user=request.user)]
    else:
        basket = [item.product_id for item in Cart.objects.filter(session_key = request.session.session_key)]
        favourites = [item.product_id for item in Like.objects.filter(session_key = request.session.session_key)]

    context: dict = {
        'title': 'Chapter & Verse - Главная',
        'categories': categories,
        'manga': manga,
        'new': new,
        'basket': basket,
        'favourites': favourites,
        'modal_form': modal_form,
        'redirect_anchor': redirect_anchor
    }

    return render(request, 'main/index.html', context)

def about(request):

    modal_form, redirect_anchor = handle_contact_form(request)

    context: dict = {
        'title': 'Chapter & Verse - О нас',
        'modal_form': modal_form,
        
    }
    return render(request, 'main/about.html', context)

def sales(request):
    modal_form, redirect_anchor = handle_contact_form(request)

    context: dict = {
        'title': 'Chapter & Verse - Акции',
        'modal_form': modal_form
    }
    return render(request, 'main/sales.html', context)

def else_(request):
    modal_form, redirect_anchor = handle_contact_form(request)

    context: dict = {
        'title': 'Chapter & Verse - Что еще почитать?',
        'modal_form': modal_form
    }
    return render(request, 'main/else.html', context)

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

# def contact_view(request):
#     if request.method == 'POST':
#         modal_form = ContactForm(request.POST)
#         if modal_form.is_valid():
#             # Отправка письма
#             first_name = modal_form.cleaned_data['first_name']
#             username = modal_form.cleaned_data['username']
#             message = modal_form.cleaned_data['message']
#             send_contact_email(first_name, username, message)

#             messages.success(request, "Сообщение успешно отправлено!")
#             redirect_anchor = "#contacts"
            
#             return render(request, 'main/index.html', {'redirect_anchor': redirect_anchor})
#             # return HttpResponseRedirect(request.path, '#contacts')
#             # return redirect(request.path + '#contacts')  # Перенаправление на главную
#     else:
#         modal_form = ContactForm()

#     return redirect(request.path, {'modal_form': modal_form})
#     # return render(request, 'main/index.html', {'form': form})

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
    