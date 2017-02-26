from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        kwargs={
            'template_name': 'password_reset_confirm.html',
            'post_reset_redirect': 'login'},
        name='password_reset_confirm'),
    url(r'^active/(?P<token>[0-9A-Za-z:-]+)/$', views.active_user, name='active'),
]
