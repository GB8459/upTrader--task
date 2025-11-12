from django.contrib import admin
from .models import MenuItem

class MenuItemAdmin(admin.ModelAdmin):
    model = MenuItem



admin.site.register(MenuItem, MenuItemAdmin)
