# Generated by Django 4.2.11 on 2024-05-12 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_orderitem_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='author_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Автор'),
        ),
    ]
