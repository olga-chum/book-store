from django.urls import path

from goods import views

app_name = 'goods'

urlpatterns = [
    path('', views.catalog, name='index'),
    path('classica/', views.classica, name='classica'),
    path('product/', views.product, name='product')
]