from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter


from .views import (
    UserViewset,
    IdentityViewset,
    ProfileViewset,
    EducationViewset,
    ResearchViewset,
    CertificateViewset,
    WorkExperienceViewset,
    SkillViewset,
    BadgeViewset,
    IdentityUrlViewset,
    UserArticleViewset,
    UserArticleRisViewset,
    DeviceViewset,
    ForgetPasswordViewset,
    UserMetaDataViewset,
    login_page,
    logout_page,
    active_user
)


router = DefaultRouter()
router.register(r'forget-password', ForgetPasswordViewset, 'forget-password')
router.register(r'devices', DeviceViewset, 'devices')
router.register(r'identities', IdentityViewset, 'identities')
router.register(r'profiles', ProfileViewset, 'profiles')
router.register(r'educations', EducationViewset, 'educations')
router.register(r'researches', ResearchViewset, 'researches')
router.register(r'certificates', CertificateViewset, 'certificates')
router.register(r'work-experiences', WorkExperienceViewset, 'work-experiences')
router.register(r'skills', SkillViewset, 'skills')
router.register(r'badges', BadgeViewset, 'badges')
router.register(r'urls', IdentityUrlViewset, 'urls')
router.register(r'user-meta', UserMetaDataViewset, 'user-meta')
router.register(r'user-articles', UserArticleViewset, 'articles')
router.register(r'user-articles-ris', UserArticleRisViewset, 'articles-ris')
router.register(r'', UserViewset, 'users')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^logout$', logout_page, name='logout'),
    url(r'^login/$', login_page, name='login'),
    url(r'^active/(?P<token>[0-9A-Za-z:_\-]+)/$', active_user, name='active'),
]
