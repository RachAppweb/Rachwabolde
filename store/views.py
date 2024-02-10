from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import *
from category.models import *
from cart.models import *
from cart.views import _card_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from accounts.context_processor import averagereview
import asyncio
from accounts.models import *

# Create your views here.


def home(request):
    review =  CommentAndRating.objects.filter(
        status=True).aggregate(Avg('rating'))
    
    context = {
        'averagereview': review
    }
    return render(request, 'home.html', context)


def usage(request):
    usages = Usage.objects.all().order_by('created_at')
    context = {
        'usages': usages
    }
    return render(request, 'usage.html', context)


def store(request, category_slug=None):
    categories = None
    products = None
    products_count = 0
    if 'search' in request.GET:
        search = request.GET['search']
        product = Product.objects.filter(Q(description__icontains=search) | Q(
            prouduct_name__icontains=search), is_availabele=True).order_by('id')
        paginator = Paginator(product, 6)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        products_count = product.count()
    elif category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_availabele=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)

        products_count = products.count()

    else:

        products = Product.objects.all().filter(is_availabele=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)

        products_count = products.count()
    banners = Banners.objects.filter(is_availabel=True)
    context = {
        "products": paged_product,
        "product_count": products_count,
        'banners': banners
        # "in_card":in_card,
    }
    return render(request, 'store.html', context)


def product_details(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_card_id(
            request), product=single_product).exists()
    except Exception as e:
        raise e
    product_gallery = productGallary.objects.filter(
        product_id=single_product.id)
    context = {"single_product": single_product,
               "in_cart": in_cart,
               'product_gallery': product_gallery

               }
    return render(request, 'product_details.html', context)


# def add_to_card(reuest):
#     return render(reuest,'add_to_card.html')
