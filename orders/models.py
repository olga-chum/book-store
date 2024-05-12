from django.db import models
from goods.models import Products

from users.models import User

class OrderitemQueryset(models.QuerySet):
    
    def full_price(self):
        return sum(cart.full_price() for cart in self)
    
    def full_discount(self):
        return sum(cart.full_discount() for cart in self)

    def total_price(self):
        return sum(cart.product_price() for cart in self)


class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name="Пользователь", default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    delivery_address = models.TextField(null=True, blank=True, verbose_name="Адрес доставки")
    flat = models.CharField(null=True, blank=True, verbose_name='Квартира или офис')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий к заказу')
    payment_on_get = models.BooleanField(default=False, verbose_name="Оплата при получении")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    status = models.CharField(max_length=50, default='В обработке', verbose_name="Статус заказа")
    qr_image = models.ImageField(upload_to='qr_codes/', null=True, blank=True, verbose_name="QR-код")  # Новое поле для QR-кода

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(to=Products, on_delete=models.SET_DEFAULT, null=True, verbose_name="Продукт", default=None)
    name = models.CharField(max_length=150, verbose_name="Название")
    author_name = models.CharField(max_length=150, verbose_name='Автор')
    price = models.DecimalField(max_digits=7, decimal_places=0, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")

    class Meta:
        db_table = "order_item"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"

    objects = OrderitemQueryset.as_manager()

    def products_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"Товар {self.name} | Заказ № {self.order.pk}"