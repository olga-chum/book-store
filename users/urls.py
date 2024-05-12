from django.urls import path

from users import views

app_name='users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('personality/', views.personality, name='personality'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    # path('my_orders/', views.my_orders, name='my_orders'),
    path('users-cart/', views.users_cart, name='users_cart'),
    path('like/', views.like, name='like'),
]