from django.contrib import admin
from django.utils.html import format_html

from organizations.models import Organization, StaffCount, Picture,\
    UserAgent


class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    list_display = ['organ_name', 'user', 'name', 'national_code', 'country',
                    'province', 'ownership_type']


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


class UserAgentAdmin(admin.ModelAdmin):
    model = UserAgent
    list_display = ['organization', 'user']


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(StaffCount, StaffCountAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(UserAgent, UserAgentAdmin)
