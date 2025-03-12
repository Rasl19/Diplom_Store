from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from products.admin import BasketAdmin


class MyUserAdmin(UserAdmin):
    model = MyUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('image', 'sex')}),
    )
    inlines = (BasketAdmin,)


admin.site.register(MyUser, MyUserAdmin)
