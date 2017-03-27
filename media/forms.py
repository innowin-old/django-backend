from django.forms import ModelForm

from media.models import Media

class MediaForm(ModelForm):

    class Meta:
        model = Media
        exclude = ['create_time']

