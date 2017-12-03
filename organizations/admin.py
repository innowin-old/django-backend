from django.contrib import admin
from django.utils.html import format_html

from organizations.models import Organization, StaffCount, Picture


class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    list_display = ['owner', 'show_admins', 'username', 'official_name', 'province', 'ownership_type', 'business_type']

    def show_admins(self, obj):
        return ", ".join([su.username for su in obj.admins.all()])


class StaffCountAdmin(admin.ModelAdmin):
    model = StaffCount
    list_display = ['organization', 'count']


class PictureAdmin(admin.ModelAdmin):
    model = Picture
    list_display = ['organization', 'order', 'picture_link']

    def picture_link(self, obj):
        return format_html(
            "<a href='%s'>%s</a>" %
            (obj.picture.file.url, obj.picture.file.url))


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(StaffCount, StaffCountAdmin)
admin.site.register(Picture, PictureAdmin)
