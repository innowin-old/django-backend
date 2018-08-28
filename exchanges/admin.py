from django.contrib import admin
from .models import Exchange, ExchangeIdentity

class ExchangeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner']

# Register your models here.
admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(ExchangeIdentity)
