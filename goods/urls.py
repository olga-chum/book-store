from django.urls import path

from goods import views

app_name = 'goods'

urlpatterns = [
    path('search/', views.catalog, name='search'),
    path('bestsellers/', views.bestsellers, name='bestsellers'),
    path('new/', views.new, name='new'),
    path('<slug:category_slug>/', views.catalog, name='index'),
    # path('product/<int:product_id>/', views.product, name='product'),
    path('product/<slug:product_slug>/', views.product, name='product')
]