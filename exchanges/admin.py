from django.contrib import admin
from .models import Exchange, ExchangeIdentity

# Register your models here.
admin.site.register(Exchange)
admin.site.register(ExchangeIdentity)