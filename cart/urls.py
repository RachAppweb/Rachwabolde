from django.urls import path
from . import views

urlpatterns = [
    path('', views.card, name='card'),
    path('add_to_card/<int:product_id>/',
         views.add_to_card, name='add_to_card'),
    path('decrement_card/<int:product_id>/<int:cart_itme_id>/',
         views.decrement_card, name='decrement_card'),
    path('remove_card/<int:product_id>/<int:cart_itme_id>/',
         views.remove_card, name='remove_card'),
    path('checkout/', views.checkout, name='checkout'),
    path('exception/', views.exception, name='exception'),
]
