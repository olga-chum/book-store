from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render
# import qrcode

from carts.models import Cart

from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem

from io import BytesIO
from django.core.files.base import ContentFile
from django.urls import reverse
from carts.utils import get_user_carts

@login_required
def create_order(request):

    if request.method == 'POST':
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
                        # first_name = form.cleaned_data['first_name'],
                        # last_name = form.cleaned_data['last_name'],
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
                            price=price,
                            quantity=quantity,
                        )

                        product.quantity -= quantity  # Уменьшение количества товара
                        product.save()  # Сохранение изменений в базе данных

                        total_amount += price * quantity  # Добавление к общей сумме

                    # # Генерация QR-кода
                    # total_amount_in_cents = int(total_amount * 100)

                    # qr_data = (
                    #     f"ST00012|Name=Спорт Лайн|PersonalAcc=40817810711524044721|"
                    #     f"BankName=ВТБ|BIC=043601968|CorrespAcc=30101810422023601968|"
                    #     f"Currency=RUB|Sum={total_amount_in_cents}|Purpose=Оплата заказа №{order.id}"
                    # )

                    # buffer = BytesIO()
                    # qr = qrcode.make(qr_data)
                    # qr.save(buffer, format="PNG")

                    # qr_image_file = ContentFile(buffer.getvalue(), 'qr_code.png')  # Создание файла
                    # order.qr_image.save('qr_code.png', qr_image_file, save=True)

                    cart_items.delete()  # Очистка корзины после заказа

                    # messages.success(request, "Заказ успешно оформлен!")  # Уведомление

                    # # Перенаправление на страницу с QR-кодом
                    # return redirect(reverse("orders:qr_code", kwargs={'order_id': order.id}))
                    return redirect('user:profile')  

            except ValidationError as e:
                messages.warning(request, str(e))
                return redirect("orders:create_order")

    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.username,
            'phone_number': request.user.phone_number
            }

        form = CreateOrderForm(initial=initial)

    # Обработка GET-запроса

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
    }
    return render(request, 'orders/create_order.html', context)