from django.contrib import admin
from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    view_on_site = True
    list_display = ('pk', 'username', 'mobile_phone')
