from django.contrib import admin
from django.utils.html import format_html

from organizations.models import Organization, StaffCount, OrganizationPicture


class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    list_display = ['owner', 'show_admins', 'username', 'official_name', 'province', 'ownership_type', 'business_type']

    def show_admins(self, obj):
        return ", ".join([su.username for su in obj.admins.all()])


class StaffCountAdmin(admin.ModelAdmin):
    model = StaffCount
    list_display = ['staff_count_organization', 'count']


class OrganizationPictureAdmin(admin.ModelAdmin):
    model = OrganizationPicture
    list_display = ['picture_organization', 'order', 'picture_link']

    def picture_link(self, obj):
        return format_html(
            "<a href='%s'>%s</a>" %
            (obj.picture.file.url, obj.picture.file.url))


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(StaffCount, StaffCountAdmin)
admin.site.register(OrganizationPicture, OrganizationPictureAdmin)
