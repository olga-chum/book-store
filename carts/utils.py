from carts.models import Cart, Like

def get_user_carts(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)
    
    if not request.session.session_key:
        request.session.create()
    return Cart.objects.filter(session_key=request.session.session_key).select_related('product')

def get_user_likes(request):
    if request.user.is_authenticated:
        return Like.objects.filter(user=request.user)
    
    if not request.session.session_key:
        request.session.create()
    return Like.objects.filter(session_key=request.session.session_key).select_related('product')