from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):
    model = MyUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('image', 'sex')}),
    )


admin.site.register(MyUser, MyUserAdmin)
