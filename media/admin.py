from django.contrib import admin
from django.utils.html import format_html

from media.models import Media


class MediaAdmin(admin.ModelAdmin):
    model = Media
    list_display = ['uploader', 'file_link', 'create_time']

    def file_link(self, obj):
        return format_html(
            "<a href='%s'>%s</a>" %
            (obj.file.url, obj.file.url))


admin.site.register(Media, MediaAdmin)
