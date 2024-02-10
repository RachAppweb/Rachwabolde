from django.shortcuts import render, redirect, get_object_or_404
from . models import *
from .forms import *
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.contrib import auth, messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from cart.models import *
from cart.views import _card_id
from store.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from .context_processor import averagereview
import asyncio
from orders.models import *

# Create your views here.


def register(request):
    # form=RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['confirm_password']

            usere = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)

            usere.phone_number = phone_number

            usere.save()  # no need to this but I just want to do it
            current_site = get_current_site(request)
            mail_subject = 'المرجو تفعيل حسابك'
            message = render_to_string('verification_email.html', {
                'user': usere,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(usere.pk)),
                'token': default_token_generator.make_token(usere)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            if usere.is_active == True:
                return redirect('store')
            else:
                return render(request, 'go_activate.html', {'user': usere})

    else:

        form = RegistrationForm()
        # print(form.errors)
    context = {
        'form': form
    }

    return render(request, 'register.html', context)
# nnnn


def login(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:

            try:
                cart = Cart.objects.get(cart_id=_card_id(request))
                cart_item = CartItem.objects.filter(cart=cart)
                for one in cart_item:
                    producte = one.product
                    try:
                        is_cart_existe = CartItem.objects.filter(
                            product=producte.id, cart=cart).exists()
                        if is_cart_existe:
                            cart_itmo = CartItem.objects.get(
                                product=producte, user=user)
                            cart_itmo.quantity += 1
                            if producte.stock >= cart_itmo.quantity:
                                cart_itmo.save()
                            else:
                                messages.warning(
                                    request, f'إن المنتج الذي تحاول إضافته إلى سلتك قد نفذ من مخزوننا')
                            HttpResponseRedirect('card')
                    except ObjectDoesNotExist:
                        cart_itmo = CartItem.objects.create(
                            product=producte, cart=cart, quantity=1)
                        cart_itmo.user = user
                        if producte.stock >= cart_itmo.quantity:
                            cart_itmo.save()
                        else:
                            messages.warning(
                                request, f'The product with the name {producte.prouduct_name} you are trying to add has reach its limit')
                            HttpResponseRedirect('card')
                #
            except:
                pass
            auth.login(request, user)
            smsg = 'go to store '
            return JsonResponse(dict(smsg=smsg), safe=False, content_type='application/json')
        else:
            msg = 'The login credential are invalid'
            return JsonResponse(dict(msg=msg), safe=False)
    return HttpResponseRedirect(url)
#


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except (TypeError, ValueError, Account.DoesNotExist, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True

        user.save()

        try:
            cart = Cart.objects.get(cart_id=_card_id(request))
            cart_item = CartItem.objects.filter(cart=cart)
            for one in cart_item:
                producte = one.product
                try:
                    is_cart_existe = CartItem.objects.filter(
                        product=producte.id, cart=cart).exists()
                    if is_cart_existe:
                        cart_itmo = CartItem.objects.get(
                            product=producte, user=user)
                        cart_itmo.quantity += 1
                        if producte.stock >= cart_itmo.quantity:
                            cart_itmo.save()
                        else:
                            messages.warning(
                                request, f'إن المنتج الذي تحاول إضافته إلى سلتك قد نفذ من مخزوننا')
                        HttpResponseRedirect('card')
                except ObjectDoesNotExist:
                    cart_itmo = CartItem.objects.create(
                        product=producte, cart=cart, quantity=1)
                    cart_itmo.user = user
                    if producte.stock >= cart_itmo.quantity:
                        cart_itmo.save()
                    else:
                        messages.warning(
                            request, f'إن المنتج الذي تحاول إضافته إلى سلتك قد نفذ من مخزوننا')
                        HttpResponseRedirect('card')
            #
        except:
            pass
         #
        auth.login(request, user)
        return redirect('dashboard')

    else:
        return redirect('register')


def resetpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        is_existe = Account.objects.filter(email=email).exists()
        if is_existe:
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = 'إعادة تعيين كلمة السر الخاصة بك'
            message = render_to_string('resting_password_by_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return redirect('/RachWAbOld/store/?reset=success')
        else:
            messages.error(
                request, 'البريد الذي أدخلت غير موجود')
            return redirect('resetpassword')

    return render(request, 'reset_password.html')


def reset_password_activation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, Account.DoesNotExist, OverflowError):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return redirect('resetnewpassword')
    else:
        # messages.error(request,)
        return redirect('/RachWAbOld/store/?reset=error')


def resetnewpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            messages.error(
                request, 'password and confirm_password does not match')
            return redirect('resetnewpassword')
        else:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            return redirect('/RachWAbOld/store/?reset=newpass')
    else:
        return render(request, 'resetnewpassword.html')

    # return render(request, 'resetnewpassword.html')


@login_required(login_url='home')
def dashboard(request):
    order = Order.objects.filter(user_id=request.user.id, is_ordered=True)
    ordercount = order.count()
    profil_form, created = UserProfile.objects.get_or_create(user=request.user)
    context = {
        'ordercount': ordercount,
        'profil_form': profil_form
    }

    return render(request, 'dashboard.html', context)


@login_required(login_url='home')
def editprofile(request):
    userprofile, created = UserProfile.objects.get_or_create(
        user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('editprofile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        "user_form": user_form,
        "profile_form": profile_form
    }

    return render(request, 'account/editprofile.html', context)


@login_required(login_url='home')
def logout(request):
    auth.logout(request)
    return redirect('home')


def comments(request):
    url = request.META.get('HTTP_REFERER')

    comm = CommentAndRating.objects.filter(status=True).order_by('-created_at')
    countcomm = comm.count()
    if request.method == 'POST':
        try:
            review, created = CommentAndRating.objects.get_or_create(
                user=request.user)
            form = CommentswithRatings(request.POST, instance=review)
            form.save()
            return redirect(url)

        except CommentAndRating.DoesNotExist:
            form = CommentswithRatings(request.POST)
            if form.is_valid():
                theuser_id = request.user
                review = form.cleaned_data['review']
                rating = form.cleaned_data['rating']

                data = CommentAndRating(
                    user=theuser_id, review=review, rating=rating)

                data.save()
                messages.success(request, 'your review has been submited')

                return redirect('comments')

    context = {
        'comment': comm,
        'count': countcomm,


    }

    return render(request, 'account/comments.html', context)


@login_required(login_url='home')
def resetpassworddasboard(request):

    profil_form, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        current_password = request.POST['currentpassword']
        new_password = request.POST['newpassword']
        confirm_password = request.POST['confirmnewpassword']
        theuser = Account.objects.get(username__exact=request.user.username)
        if new_password != confirm_password:
            messages.error(
                request, 'كلمة السر وتأكيد كلمة السر لا يتطابقان ')
            return redirect('resetpassworddasboard')
        else:
            success = theuser.check_password(current_password)
            if success:
                theuser.set_password(new_password)
                theuser.save()
                messages.success(
                    request, 'كلمة السر الخاصة بك تم تغييرها بنجاح ')
                return redirect('resetpassworddasboard')
            else:
                messages.error(request, 'please enter a valid info ')
                return redirect('resetpassworddasboard')

    context = {
        'profil_form': profil_form
    }

    return render(request, 'account/dashpass.html', context)


def page_notfound(request, exception):
    return render(request, 'errors/404.html')


def forbidden(request, exception):
    return render(request, 'errors/403.html')
