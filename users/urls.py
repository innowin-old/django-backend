from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter


from .views import (
    IdentityViewset,
    ProfileViewset,
    EducationViewset,
    ResearchViewset,
    CertificateViewset,
    WorkExperienceViewset,
    SkillViewset,
    BadgeViewset,
    login_page,
    logout_page,
    active_user
)


router = DefaultRouter()
router.register(r'identities', IdentityViewset)
router.register(r'profiles', ProfileViewset)
router.register(r'educations', EducationViewset)
router.register(r'researches', ResearchViewset)
router.register(r'certificates', CertificateViewset)
router.register(r'work-experiences', WorkExperienceViewset)
router.register(r'skills', SkillViewset)
router.register(r'badges', BadgeViewset)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^logout$', logout_page, name='logout'),
    url(r'^login/$', login_page, name='login'),
    url(r'^active/(?P<token>[0-9A-Za-z:_\-]+)/$', active_user, name='active'),
]



"""from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^logout$', views.logout_page, name='logout'),
    url(r'^login/$', views.login_page, name='login'),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        kwargs={
            'template_name': 'password_reset_confirm.html',
            'post_reset_redirect': 'login'},
        name='password_reset_confirm'),
    url(r'^active/(?P<token>[0-9A-Za-z:_\-]+)/$', views.active_user, name='active'),
]
"""
