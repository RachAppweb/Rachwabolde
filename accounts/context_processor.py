from django.shortcuts import render, redirect
from . models import *
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse, Http404
import asyncio
from store.models import Banners
# Create your views here.


def register(request):
    # form=RegistrationForm()
    context = {}
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

            if password != password2:
                return render(request, 'passdoesentmatch.html')

            else:
                usere = Account.objects.create_user(
                    first_name=first_name, last_name=last_name, email=email, username=username, password=password)

                usere.phone_number = phone_number

                usere.save()  # no need to this but I just want to do it
                return redirect('store')

    else:
        form = RegistrationForm()
        context = {
            'form': form
        }

    return context


async def averagereview(request):
    review = await CommentAndRating.objects.filter(
        status=True).aggregate(average=Avg('rating'))
    avg = 0
    if review['average'] is not None:
        avg = review['average'] or 0
        float(avg)
        # print(avg)
        last = round(avg, 2)
    return last


def banners(request):
    banners = Banners.objects.filter(is_availabel=True)
    # first_banner=Banners.objects.get(id=1)
    # first_banner=Banners.objects.get(id=1)

    return dict(banners=banners)
