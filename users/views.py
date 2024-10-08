from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import auth, messages
from django.urls import reverse
from goods.models import Categories, Products
from datetime import datetime
from carts.models import Cart, Like
from orders.models import Order, OrderItem
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm
from main.forms import ContactForm
from django.contrib import messages

from django.core.mail import send_mail

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password, backend='modules.system.backends.EmailAuthBackend')
            session_key = request.session.session_key
            if user:
                auth.login(request, user)
                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)
                    Like.objects.filter(session_key=session_key).update(user=user)
                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))
                
                return HttpResponseRedirect(reverse('user:profile'))
        else:
            # Возвращаем страницу, которая содержит модальное окно, с контекстом, чтобы показать ошибки
            categories = Categories.objects.all()
            manga = Products.objects.filter(category__slug='Manga').order_by('?')[:6]
            new = Products.objects.filter(year_of_publish=datetime.now().year).order_by('?')[:6]

            context: dict = {
                'form': form,
                'title': 'Chapter & Verse - Главная',
                'categories': categories,
                'manga': manga,
                'new': new
            }
            return render(request, 'main/index.html', context)  # Шаблон, который содержит модальное окно

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.phone_number = form.cleaned_data.get('phone_number')           
            user.save()
            user = form.instance
            
            session_key = request.session.session_key
            
            # Авторизуем пользователя
            auth.login(request, user)
            
            if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)
                    Like.objects.filter(session_key=session_key).update(user=user)
            
            return HttpResponseRedirect(reverse('user:profile'))
        else:
            # Возвращаем страницу, которая содержит модальное окно, с контекстом, чтобы показать ошибки
            categories = Categories.objects.all()
            manga = Products.objects.filter(category__slug='Manga').order_by('?')[:6]
            new = Products.objects.filter(year_of_publish=datetime.now().year).order_by('?')[:6]

            context: dict = {
                'form': form,
                'title': 'Chapter & Verse - Главная',
                'categories': categories,
                'manga': manga,
                'new': new
            }
            return render(request, 'main/index.html', context)  # Шаблон, который содержит модальное окно


@login_required
def profile(request):
    form = ProfileForm(instance=request.user)
    modal_form, redirect_anchor = handle_contact_form(request)
    if request.user.is_authenticated:
        basket = [item.product_id for item in Cart.objects.filter(user=request.user)]
        select = Like.objects.filter(user=request.user)[:5]
        favourites = [item.product_id for item in Like.objects.filter(user=request.user)]
    else:
        basket = [item.product_id for item in Cart.objects.filter(session_key = request.session.session_key)]
        select = Like.objects.filter(session_key = request.session.session_key)[:5]
        favourites = [item.product_id for item in Like.objects.filter(session_key = request.session.session_key)]

    orders = (
        Order.objects.filter(user=request.user).exclude(status__in=['Выполнен', 'Отменен'])
            .prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product")
                )
            )
            .order_by("-id")[:1]
    )

    context = {
        "title": "Chapter & Verse - Профиль", 
        'form': form,
        'select': select,
        'favourites': favourites,
        'basket': basket,
        "orders": orders,
        'modal_form': modal_form,
        'redirect_anchor': redirect_anchor
        
    }
    return render(request, 'users/profile.html', context)  # Шаблон, который содержит модальное окно

@login_required
def personality(request):
    form = ProfileForm(instance=request.user)
    modal_form = ContactForm()
    redirect_anchor = None

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'profile_form':
            form = ProfileForm(data=request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('users:personality'))
                   
        elif form_type == 'contact_form':
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

    context = {
        'title': 'Chapter & Verse - Личные данные',
        'form': form,
        'modal_form': modal_form,
        'redirect_anchor': redirect_anchor
        
    }
    return render(request, 'users/personality.html', context)

@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))

@login_required
def my_orders(request):
    form = ProfileForm(instance=request.user)
    modal_form, redirect_anchor = handle_contact_form(request)

    orders = (
            Order.objects.filter(user=request.user).prefetch_related(
                Prefetch(
                    'orderitem_set',
                    queryset=OrderItem.objects.select_related('product')
                )
            ).order_by('-id')
        )

    context = {
        "title": "Chapter & Verse - Мои заказы", 
        'form': form,
        'orders': orders,
        'modal_form': modal_form,
        'redirect_anchor': redirect_anchor
        
        }
    return render(request, "users/my_orders.html", context)

def users_cart(request):
    modal_form, redirect_anchor = handle_contact_form(request)
    if request.user.is_authenticated:
        favourites = [item.product_id for item in Like.objects.filter(user=request.user)]
    else:
        favourites = [item.product_id for item in Like.objects.filter(session_key = request.session.session_key)]
    
    context = {
        "title": "Chapter & Verse - Корзина", 
        'favourites': favourites,
        'modal_form': modal_form,
        'redirect_anchor': redirect_anchor
        }
    return render(request, "users/users_cart.html", context)

def like(request):
    modal_form, redirect_anchor = handle_contact_form(request)
    if request.user.is_authenticated:
        basket = [item.product_id for item in Cart.objects.filter(user=request.user)]
        favourites = [item.product_id for item in Like.objects.filter(user=request.user)]
    else:
        basket = [item.product_id for item in Cart.objects.filter(session_key = request.session.session_key)]
        favourites = [item.product_id for item in Like.objects.filter(session_key = request.session.session_key)]
    
    context = {
        "title": "Chapter & Verse - Избранное",
        'basket': basket, 
        'favourites': favourites,
        'modal_form': modal_form,
        'redirect_anchor': redirect_anchor
        
        }
    return render(request, "users/like.html", context)

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
    