from store.models import *
from .models import Cart, CartItem
from .views import _card_id


def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}

    try:
        cart = Cart.objects.filter(cart_id=_card_id(request))
        if request.user.is_authenticated:
            cart_item = CartItem.objects.all().filter(user=request.user)
        else:
            cart_item = CartItem.objects.all().filter(cart=cart[:1])
        for cartitem in cart_item:
            cart_count += cartitem.quantity

    except Cart.DoesNotExist:
        cart_count = 0
    return dict(cart_count=cart_count)
