from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from carts.utils import get_user_carts, get_user_likes

from carts.models import Cart, Like
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

    else:
        carts = Cart.objects.filter(
            session_key = request.session.session_key, product=product)
        
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(
                session_key = request.session.session_key, product=product, quantity=1
            )    
    
    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request
    )

    response_data = {
        "cart_items_html": cart_items_html
    }

    return JsonResponse(response_data)

def cart_change(request):
    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")

    cart = Cart.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()

    cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": cart}, request=request
    )

    response_data = {
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)

def cart_remove(request):
    cart_id = request.POST.get("cart_id")

    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request
    )

    response_data = {
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity,
    }

    return JsonResponse(response_data)

def like_add(request):
    
    product_id = request.POST.get("product_id")

    product = Products.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        likes = Like.objects.filter(user=request.user, product=product)

        if likes.exists():
            like = likes.first()
            if like:
                like.save()
        else:
            Like.objects.create(user=request.user, product=product)

    else:
        likes = Like.objects.filter(
            session_key = request.session.session_key, product=product)
        
        if likes.exists():
            like = likes.first()
            if like:
                like.save()
        else:
            Like.objects.create(
                session_key = request.session.session_key, product=product
            )    
    
    user_like = get_user_likes(request)
    like_items_html = render_to_string(
        "carts/includes/included_like.html", {"likes": user_like}, request=request
    )

    response_data = {
        "like_items_html": like_items_html
    }

    return JsonResponse(response_data)

def like_remove(request):
    like_id = request.POST.get("like_id")

    like = Like.objects.get(id=like_id)
    like.delete()

    user_like = get_user_likes(request)
    like_items_html = render_to_string(
        "carts/includes/included_like.html", {"likes": user_like}, request=request
    )

    response_data = {
        "like_items_html": like_items_html,
    }

    return JsonResponse(response_data)