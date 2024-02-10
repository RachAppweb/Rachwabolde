from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import *
from store.models import *
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


def _card_id(request):
    card = request.session.session_key

    if not card:

        card = request.session.create()
    return card


def _is_ajax(request):
    return request.META.get('HTTP_H_REQUESTED_WITH') == 'XMLHttpRequest'


def add_to_card(request, product_id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    product = Product.objects.get(id=product_id)
# ----logged in user
    if product.stock >= 1:
        if current_user.is_authenticated:

            # if request.method == 'POST':
            is_existe = CartItem.objects.filter(
                product=product, user=current_user).exists()
            if is_existe:
                cart_item = CartItem.objects.get(
                    product=product, user=current_user)
                cart_item.quantity += 1
                if product.stock >= cart_item.quantity:

                    cart_item.save()
                else:
                    messages.warning(
                        request, f'إن المنتج الذي تحاول إضافته إلى سلتك قد نفذ من مخزوننا')
                    return redirect(url)
            else:
                cart_item = CartItem.objects.create(
                    product=product, quantity=1, user=current_user)
                if product.stock >= cart_item.quantity:
                    cart_item.save()
                else:
                    messages.warning(
                        request, f'إن المنتج الذي تحاول إضافته إلى سلتك قد نفذ من مخزوننا')
                    return redirect(url)
            return redirect('card')
            # ----non logged in user
        else:
            # if request.method == 'POST':
            try:
                cart = Cart.objects.get(cart_id=_card_id(request))

            except Cart.DoesNotExist:
                cart = Cart.objects.create(cart_id=_card_id(request))
            cart.save()
            is_existe = CartItem.objects.filter(
                product=product, cart=cart).exists()
            if is_existe:
                cart_item = CartItem.objects.get(
                    product=product, cart=cart)

                cart_item.quantity += 1
                if product.stock >= cart_item.quantity:
                    cart_item.save()
                else:
                    messages.warning(
                        request, f'إن المنتج الذي تحاول إضافته إلى سلتك قد نفذ من مخزوننا')
                    return redirect(url)

            else:
                cart_item = CartItem.objects.create(
                    product=product, quantity=1, cart=cart)

                if product.stock >= cart_item.quantity:
                    cart_item.save()
                else:
                    messages.warning(
                        request, f'إن المنتج الذي تحاول إضافته إلى سلتك قد نفذ من مخزوننا')
                    return redirect(url)
            return redirect('card')
    else:
        messages.warning(
            request, 'إن المنتج الذي تحاول إضافته إلى سلتك قد نفذ من مخزوننا')
        return redirect(url)
    # redirect('card')

# ////


def decrement_card(request, product_id, cart_itme_id):

    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, user=request.user, id=cart_itme_id)

        else:
            card = Cart.objects.get(cart_id=_card_id(request))
            cart_item = CartItem.objects.get(
                product=product, cart=card, id=cart_itme_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1

            cart_item.save()

        else:
            cart_item.delete()

    except:
        pass
    return redirect('card')


def remove_card(request, product_id, cart_itme_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(
            product=product, user=request.user, id=cart_itme_id)
    else:

        card = Cart.objects.get(cart_id=_card_id(request))

        cart_item = CartItem.objects.get(
            product=product, cart=card, id=cart_itme_id)

    product.save()
    cart_item.delete()
    return redirect('card')


def card(request, total=0, quantity=0, cart_itmes=None):
    finaltotal = 0
    deliver = 0
    try:
        if request.user.is_authenticated:
            cart_itmes = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_card_id(request))
            cart_itmes = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_itmes:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            # deliver=50
            if cart_item.quantity > 0:
                deliver = 5
            else:
                deliver = 0
            finaltotal = total+deliver
    except ObjectDoesNotExist:
        pass
    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_itmes,
        "finaltotal": finaltotal,
        "deliver": deliver
    }
    # if _is_ajax(request=request):
    #     return JsonResponse(context, safe=False)
    return render(request, 'add_to_card.html', context)


@login_required(login_url='exception')
def checkout(request, total=0, quantity=0, cart_itmes=None):
    try:
        if request.user.is_authenticated:
            cart_itmes = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_card_id(request))
            cart_itmes = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_itmes:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_itmes
    }
    return render(request, 'checkout.html', context)


def exception(request):
    return render(request, 'exception.html')
