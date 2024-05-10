from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse
from carts.utils import get_user_carts

from carts.models import Cart
# from carts.utils import get_user_carts
from goods.models import Products

def cart_add(request):
    
    product_id = request.POST.get("product_id")

    product = Products.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart :
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request
    )

    response_data = {
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)    

def is_item_in_cart(user, product_slug):
    # Проверяем наличие товара с указанным product_id в корзине пользователя
    return Cart.objects.filter(user=user, slug=product_slug).exists()

def cart_change(request, product_slug):
    ...

def cart_remove(request):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()

    return redirect(request.META['HTTP_REFERER'])