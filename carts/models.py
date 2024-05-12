from django.db import models
from users.models import User
from goods.models import Products

class CartQueryset(models.QuerySet):

    def full_price(self):
        return sum(cart.full_price() for cart in self)
    
    def full_discount(self):
        return sum(cart.full_discount() for cart in self)

    def total_price(self):
        return sum(cart.product_price() for cart in self)

class Cart(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'cart'
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
        ordering = ("id",)

    objects = CartQueryset().as_manager()

    def full_price(self):
        return self.product.price * self.quantity
    
    def full_discount(self):
        return  round((self.product.price * self.product.discount // 100), 2) * self.quantity
    
    def product_price(self):
        return round(self.product.sell_price() * self.quantity, 0)

    def __str__(self):
        if self.user:
            return f'Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}'
        
        return f'Анонимная корзина | Товар {self.product.name} | Количество {self.quantity}'
    

class Like(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name='Товар')
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'like'
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        if self.user:
            return f'Избранное {self.user.username} | Товар {self.product.name}'
        
        return f'Анонимное избранное | Товар {self.product.name}'