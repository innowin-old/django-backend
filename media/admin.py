from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from media.models import Media


class MediaAdmin(admin.ModelAdmin):
    model = Media
    list_display = ['uploader', 'file_link', 'create_time']
    readonly_fields = ['file_image']

    def file_link(self, obj):
        return format_html(
            "<a href='%s'>%s</a>" %
            (obj.file.url, obj.file.url))

    def file_image(self, obj):
        return mark_safe('<img src="{url}" width="300" />'.format(
            url=obj.file.url,
            )
        )


admin.site.register(Media, MediaAdmin)
