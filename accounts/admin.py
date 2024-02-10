from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
# Register your models here.


class AdminAccount(UserAdmin):
    list_display = ['email', 'first_name', 'last_name',
                    'username', 'last_login', 'date_joined', 'is_active']
    list_display_links = ('email', 'username')
    readonly_fields = ('last_login', 'date_joined')
    filter_horizontal = ()
    ordering = ['-date_joined']
    list_filter = ()
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.profil_picture:
            return format_html('<img src="{}" width=30 style="border-radius:50%;">'.format(object.profil_picture.url))
        else:
            return 'no image'
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')


admin.site.register(Account, AdminAccount)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CommentAndRating)
admin.site.register(MessagesFromUs)
