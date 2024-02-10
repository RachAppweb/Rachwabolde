from django.db import models
from .models import *
from category.models import *
from django.urls import reverse
# Create your models here.


class Product(models.Model):
    prouduct_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_availabele = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # @property
    def availability(self):
        if self.stock <= 0:
            self.is_availabele = False
        else:
            self.is_availabele = True

    def save(self, *args, **kwargs):
        self.availability()
        super().save(*args, **kwargs)

    def get_pro_url(self):
        return reverse("product_details", args=[self.category.slug, self.slug])

    def __str__(self):
        return self.prouduct_name


class productGallary(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='stor/product')

    def __str__(self):
        return self.product.prouduct_name


class Banners(models.Model):
    images = models.ImageField(upload_to='store/banners')
    is_availabel = models.BooleanField(default=True)

    def __str__(self):
        return 'Images'


class Usage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=700, blank=True)
    screen = models.ImageField(upload_to='stor/usage')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at.strftime('%d-%m-%Y')}"
