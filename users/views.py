from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import auth, messages
from django.urls import reverse
from goods.models import Categories, Products
from datetime import datetime

# from carts.models import Cart
# from orders.models import Order, OrderItem
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm

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
                # if session_key:
                #     Cart.objects.filter(session_key=session_key).update(user=user)
                if request.POST.get('next', None):
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
            # # if session_key:
            # #         Cart.objects.filter(session_key=session_key).update(user=user)
            
            session_key = request.session.session_key
            # Авторизуем пользователя
            auth.login(request, user)
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

    context = {
        "title": "Chapter & Verse - Профиль", 
        'form': form,
    }
    return render(request, 'users/profile.html', context)  # Шаблон, который содержит модальное окно

@login_required
def personality(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:personality'))
        else:
            context = {
                'form': form
            }
    else:
        form = ProfileForm(instance=request.user)

    context = {
        'title': 'Chapter & Verse - Личные данные',
        'form': form,
    }
    return render(request, 'users/personality.html', context)

@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))

# def my_orders(request):

#     if request.method == 'POST':
#         form = ProfileForm(data=request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f" Профиль успешно обновлен ")
#             return HttpResponseRedirect(reverse('user:profile'))
#         else:
#             # Возвращаем страницу, которая содержит модальное окно, с контекстом, чтобы показать ошибки
#             context = {
#                 'form': form
#             }
#     else:
#         form = ProfileForm(instance=request.user)

#     orders = (
#             Order.objects.filter(user=request.user).prefetch_related(
#                 Prefetch(
#                     'orderitem_set',
#                     queryset=OrderItem.objects.select_related('product')
#                 )
#             ).order_by('-id')
#         )
    
#     for order in orders:
#         order.total_price = order.orderitem_set.aggregate(total=Sum(F('price') * F('quantity')))['total']

#     context = {
#         "title": "Chapter & Verse - Мои заказы", 
#         'form': form,
#         'orders': orders,
#         }
#     return render(request, "users/my_orders.html", context)

# def users_cart(request):
#     context = {
#         "title": "Chapter & Verse - Корзина", 
#         }
#     return render(request, "users/users_cart.html", context)


