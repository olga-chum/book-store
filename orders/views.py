from django.shortcuts import render
from carts.utils import get_user_carts

def create_order(request):
    carts = get_user_carts(request)
    total_price = sum(cart.full_price() for cart in carts)
    total_discount = sum(cart.full_discount() for cart in carts)
    total_price_with_discount = total_price - total_discount
    
    context = {
        'carts': carts,
        'total_price': total_price,
        'total_discount': total_discount,
        'total_price_with_discount': total_price_with_discount,
    }
    return render(request, 'orders/create_order.html', context)