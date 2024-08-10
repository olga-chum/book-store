from email.mime import image
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render
import qrcode

from io import BytesIO
from django.core.files.base import ContentFile
from django.urls import reverse

from carts.models import Cart

from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem

from carts.utils import get_user_carts
from main.forms import ContactForm
from django.contrib import messages

from django.core.mail import send_mail


@login_required
def create_order(request):
    initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.username,
            'phone_number': request.user.phone_number
            }

    form = CreateOrderForm(initial=initial)
    modal_form = ContactForm()
    redirect_anchor = None

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'contact_form':
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
        
        elif form_type == 'profile_form':
            form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():  # Обеспечение атомарности операции
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)

                    if not cart_items.exists():
                        messages.warning(request, "Ваша корзина пуста.")
                        return redirect("goods:catalog")

                    # Создание заказа
                    order = Order.objects.create(
                        user=user,
                        first_name = form.cleaned_data['first_name'],
                        last_name = form.cleaned_data['last_name'],
                        phone_number=form.cleaned_data['phone_number'],
                        delivery_address=form.cleaned_data['delivery_address'],
                        flat=form.cleaned_data.get('flat', None),
                        # payment_on_get=form.cleaned_data['payment_on_get'],
                        comment=form.cleaned_data.get('comment', None),
                    )

                    total_amount = 0  # Общая сумма заказа

                    # Создание заказанных товаров
                    for cart_item in cart_items:
                        product = cart_item.product
                        name = cart_item.product.name
                        author_name = cart_item.product.author_name
                        image = cart_item.product.image
                        price = cart_item.product.sell_price()
                        quantity = cart_item.quantity

                        if product.quantity < quantity:
                            raise ValidationError(f"Недостаточно товара {name}. В наличии - {product.quantity}")

                        # Создание `OrderItem` для каждого товара в корзине
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            author_name=author_name,
                            name=name,
                            image = image,
                            price=price,
                            quantity=quantity,
                        )

                        product.quantity -= quantity  # Уменьшение количества товара
                        product.save()  # Сохранение изменений в базе данных

                        total_amount += price * quantity  # Добавление к общей сумме

                    # Генерация QR-кода
                    total_amount_in_cents = int(total_amount * 100)

                    qr_data = (
                        f"ST00012|Name=ИП Чумакова О.Р.|PersonalAcc=40817810600089220095|"
                        f"BankName=Тинькофф Банк|BIC=044525974|CorrespAcc=30101810145250000974|"
                        f"Currency=RUB|Sum={total_amount_in_cents}|Purpose=Оплата заказа Chapter & Verse"
                    )

                    buffer = BytesIO()
                    qr = qrcode.make(qr_data)
                    qr.save(buffer, format="PNG")

                    qr_image_file = ContentFile(buffer.getvalue(), 'qr_code.png')  # Создание файла
                    order.qr_image.save('qr_code.png', qr_image_file, save=True)

                    cart_items.delete()  # Очистка корзины после заказа

                    # Перенаправление на страницу с QR-кодом
                    return redirect(reverse("orders:qr_code", kwargs={'order_id': order.id})) 

            except ValidationError as e:
                messages.warning(request, str(e))
                return redirect("user:users_cart")

    carts = get_user_carts(request)
    total_price = sum(cart.full_price() for cart in carts)
    total_discount = sum(cart.full_discount() for cart in carts)
    total_price_with_discount = total_price - total_discount
    
    context = {
        'carts': carts,
        'total_price': total_price,
        'total_discount': total_discount,
        'total_price_with_discount': total_price_with_discount,
        'title': 'Chapter & Verse - Оформление заказа',
        'form': form,
        'orders': True,
        'modal_form': modal_form,
        'redirect_anchor': redirect_anchor
    }
    return render(request, 'orders/create_order.html', context)

# def order(request):
#     if request.method == 'POST':
#         form = CreateOrderForm(data=request.POST)
#         if form.is_valid():
#             try:
#                 with transaction.atomic():  # Обеспечение атомарности операции
#                     user = request.user
#                     cart_items = Cart.objects.filter(user=user)

#                     if not cart_items.exists():
#                         messages.warning(request, "Ваша корзина пуста.")
#                         return redirect("goods:catalog")

#                     # Создание заказа
#                     order = Order.objects.create(
#                         user=user,
#                         first_name = form.cleaned_data['first_name'],
#                         last_name = form.cleaned_data['last_name'],
#                         phone_number=form.cleaned_data['phone_number'],
#                         delivery_address=form.cleaned_data['delivery_address'],
#                         flat=form.cleaned_data.get('flat', None),
#                         # payment_on_get=form.cleaned_data['payment_on_get'],
#                         comment=form.cleaned_data.get('comment', None),
#                     )

#                     total_amount = 0  # Общая сумма заказа

#                     # Создание заказанных товаров
#                     for cart_item in cart_items:
#                         product = cart_item.product
#                         name = cart_item.product.name
#                         author_name = cart_item.product.author_name
#                         price = cart_item.product.sell_price()
#                         quantity = cart_item.quantity

#                         if product.quantity < quantity:
#                             raise ValidationError(f"Недостаточно товара {name}. В наличии - {product.quantity}")

#                         # Создание `OrderItem` для каждого товара в корзине
#                         OrderItem.objects.create(
#                             order=order,
#                             product=product,
#                             author_name=author_name,
#                             name=name,
#                             price=price,
#                             quantity=quantity,
#                         )

#                         product.quantity -= quantity  # Уменьшение количества товара
#                         product.save()  # Сохранение изменений в базе данных

#                         total_amount += price * quantity  # Добавление к общей сумме

#                     # # Генерация QR-кода
#                     # total_amount_in_cents = int(total_amount * 100)

#                     # qr_data = (
#                     #     f"ST00012|Name=Спорт Лайн|PersonalAcc=40817810711524044721|"
#                     #     f"BankName=ВТБ|BIC=043601968|CorrespAcc=30101810422023601968|"
#                     #     f"Currency=RUB|Sum={total_amount_in_cents}|Purpose=Оплата заказа №{order.id}"
#                     # )

#                     # buffer = BytesIO()
#                     # qr = qrcode.make(qr_data)
#                     # qr.save(buffer, format="PNG")

#                     # qr_image_file = ContentFile(buffer.getvalue(), 'qr_code.png')  # Создание файла
#                     # order.qr_image.save('qr_code.png', qr_image_file, save=True)

#                     cart_items.delete()  # Очистка корзины после заказа

#                     # messages.success(request, "Заказ успешно оформлен!")  # Уведомление

#                     # # Перенаправление на страницу с QR-кодом
#                     # return redirect(reverse("orders:qr_code", kwargs={'order_id': order.id}))
#                     return redirect('user:profile')  

#             except ValidationError as e:
#                 messages.warning(request, str(e))
#                 return redirect("user:users_cart")

#     else:
#         initial = {
#             'first_name': request.user.first_name,
#             'last_name': request.user.last_name,
#             'email': request.user.username,
#             'phone_number': request.user.phone_number
#             }

#         return CreateOrderForm(initial=initial)


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

def qr_code(request, order_id):
    order = Order.objects.get(pk=order_id)  # Получение заказа по ID
    qr_image_url = order.qr_image.url if order.qr_image else None  # URL изображения QR-кода
    modal_form, redirect_anchor = handle_contact_form(request)

    context = {
        'title': 'Chapter & Verse - Оплата заказа',
        'qr_image_url': qr_image_url,  # Передача URL изображения в контекст
        'modal_form': modal_form,
    }

    return render(request, 'orders/qr_code.html', context)

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