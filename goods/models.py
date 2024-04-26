from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name 


class Products(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    author_name = models.CharField(max_length=150, null=True, blank=True, verbose_name='Автор')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Изображение')
    price = models.PositiveIntegerField(default=0, max_length=6, verbose_name='Цена')
    discount = models.PositiveIntegerField(default=0, max_length=6, null=True, verbose_name='Скидка в %')
    quantity = models.PositiveIntegerField(default=0, max_length=6, null=True, verbose_name='Количество')
    age = models.PositiveIntegerField(default=0, max_length=6, null=True, verbose_name='Возраст')
    year_of_publish = models.PositiveIntegerField(max_length=4, null=True, verbose_name='Год издания')
    publisher = models.CharField(max_length=150,null=True, verbose_name='Издательство')
    cycle = models.CharField(max_length=150, null =True, blank=True, verbose_name='Цикл')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')



    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.name} Количество - {self.quantity}'