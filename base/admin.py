from django.contrib import admin
from .models import RollPermission, Post, BaseCountry, BaseProvince, BaseTown

class PostAdmin(admin.ModelAdmin):
    list_display = ['pk', 'post_title', 'post_identity', 'post_type', 'post_user', 'post_parent']

class BaseCountryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'code']

class BaseProvinceAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'code', 'province_related_country']

class BaseTownAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'code', 'town_related_province']

# Register your models here.
admin.site.register(RollPermission)
admin.site.register(Post, PostAdmin)
admin.site.register(BaseCountry, BaseCountryAdmin)
admin.site.register(BaseProvince, BaseProvinceAdmin)
admin.site.register(BaseTown, BaseTownAdmin)
