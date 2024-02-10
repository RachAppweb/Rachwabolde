from django.urls import path
from . import views
urlpatterns = [
    path('store/', views.store, name='store'),
    path('', views.home, name='home'),
    path('usage/', views.usage, name='usage'),
    path('category/<slug:category_slug>/',
         views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',
         views.product_details, name='product_details'),

    # path('store/add_to_card/',views.add_to_card,name='add_to_card'),

]
