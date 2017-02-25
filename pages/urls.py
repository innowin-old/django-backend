from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout$', views.logout_page, name='logout'),
    url(r'^login/$', views.login_page, name='login'),
]
