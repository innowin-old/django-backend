from django.contrib import admin
from .models import Exchange, Exchange_Identity

# Register your models here.
admin.site.register(Exchange)
admin.site.register(Exchange_Identity)