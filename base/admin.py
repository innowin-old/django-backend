from django.contrib import admin
from .models import RollPermission, Post, BaseCountry, BaseProvince, BaseTown

class PostAdmin(admin.ModelAdmin):
    list_display = ['pk', 'post_title', 'post_identity', 'post_type', 'post_user', 'post_parent']

# Register your models here.
admin.site.register(RollPermission)
admin.site.register(Post, PostAdmin)
admin.site.register(BaseCountry)
admin.site.register(BaseProvince)
admin.site.register(BaseTown)
