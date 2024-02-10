from cart.models import CartItem
# from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import OrderForm
import datetime
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
import json
from store.models import Product
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import JsonResponse
# Create your views here.


def placeorder(request, total=0, quantity=0):
    current_user = request.user
    cart_itemes = CartItem.objects.filter(user=current_user)
    cart_count = cart_itemes.count()

    if cart_count <= 0:
        return redirect('store')
    # order_data=request.session.get('context')
    # if order_data:
    #     return render(request,'orders/payments.html')
    deliver = 5
    for cart_item in cart_itemes:

        total += (cart_item.product.price*cart_item.quantity)
        quantity += cart_item.quantity
    totale = total
    finaltotal = totale+deliver

    if request.method == 'POST':

        form = OrderForm(request.POST)

        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone_number = form.cleaned_data['phone_number']
            data.address_line1 = form.cleaned_data['address_line1']
            data.address_line2 = form.cleaned_data['address_line2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            # data = Order(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number,
            #              address_line1=address_line1, address_line2=address_line2, country=country, state=state, city=city)
            data.order_total = totale
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = get_object_or_404(Order,
                                      user=current_user, is_ordered=False, order_number=order_number)
            context = {
                "order": order,
                "cart_itemes": cart_itemes,
                "total": totale,
                "finaltotal": finaltotal,
                'deliver': deliver
            }
            # return redirect('payments')
            return render(request, 'orders/payments.html', context)

            # request.session['context']=context

    else:
        form = OrderForm()

        # context = {
        #     "order": order,
        #     "cart_itemes": cart_itemes,
        #     "total": totale,
        #     "finaltotal": finaltotal
        # }

    return render(request, 'checkout.html')


def payments(request):
    body = json.loads(request.body)
    # print(body)
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=body['orderid'])
    order_number = body['orderid']
    payment = Payment(
        user=request.user,
        payment_id=body['transId'],
        payment_method=body['payment_method'],
        payer_name=body['payer_name'],
        payer_surname=body['payer_surname'],
        amount_paid=body['amount_paid'],
        status=body['status']
    )
    payment.save()
    order.payment = payment
    if payment.status == 'COMPLETED':
        order.is_ordered = True
    order.save()

    cart_item = CartItem.objects.filter(user=request.user)
    for item in cart_item:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    mail_subject = 'لقد تم التوصل بطلبك'
    message = render_to_string('orders/paymentscomplet.html', {
        'user': request.user,
        'order': order,
        'cart_item': cart_item
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    CartItem.objects.filter(user=request.user).delete()
    data = {
        'order_number': order_number,
        'trnasId': payment.payment_id
    }

    return JsonResponse(data)


def invoice(request):
    order_number = request.GET.get('order_number')
    transId = request.GET.get('transId')
    print(order_number)
    print(transId)
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        order_product = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=transId)
        subtotal = 0
        deliver = 0
        finaltotal = 0
        for item in order_product:
            subtotal += item.product_price*item.quantity
            if item.quantity > 0:
                deliver = 5
            else:
                deliver = 0
            finaltotal = subtotal+deliver

        context = {
            'order': order,
            'order_product': order_product,
            'order_number': order.order_number,
            'transId': payment.payment_id,
            'amount_paid': payment.amount_paid,
            'payment': payment,
            'deliver': deliver,
            'subtotal': subtotal,
            'finaltotal': finaltotal
        }
        return render(request, 'orders/invoice.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('store')
