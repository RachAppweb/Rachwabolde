from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.


class ProductGalleryinline(admin.TabularInline):

    model = productGallary
    extra = 0
    readonly_fields = ['thumbnail']
    # exclude = ['images']

    def thumbnail(self, object):
        if object.images:
            return format_html('<img src="{}" width=40 style="border-radius:50%;">'.format(object.images.url))
        else:
            return 'no image'
    thumbnail.short_description = 'image'


class ProductAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.image:
            return format_html('<img src="{}" width=30 style="border-radius:50%;">'.format(object.image.url))
        else:
            return 'no image'
    thumbnail.short_description = 'image'
    # list_display = ['thumbnail', 'product']
    list_display = ('thumbnail', 'prouduct_name', 'price', 'stock',
                    'category', 'modified_date', 'is_availabele')

    inlines = [ProductGalleryinline]


class GallaryAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.images:
            return format_html('<img src="{}" width=30 style="border-radius:50%;">'.format(object.images.url))
        else:
            return 'no image'
    thumbnail.short_description = 'images'
    list_display = ['thumbnail', 'product']


admin.site.register(Product, ProductAdmin)
admin.site.register(productGallary, GallaryAdmin)
admin.site.register(Banners)
admin.site.register(Usage)
