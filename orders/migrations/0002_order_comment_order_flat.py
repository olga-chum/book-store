# Generated by Django 4.2.11 on 2024-05-12 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий к заказу'),
        ),
        migrations.AddField(
            model_name='order',
            name='flat',
            field=models.CharField(blank=True, null=True, verbose_name='Квартира или офис'),
        ),
    ]
