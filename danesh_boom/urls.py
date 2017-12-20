"""danesh_boom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls

import media.views
from danesh_boom.schema import schema
from .views import SafeGraphQLView

urlpatterns = [
    url(r'^users/', include('users.urls')),
    url(r'^organizations/', include('organizations.urls')),
    url(r'^products/', include('products.urls')),
    url(r'^base/', include('base.urls')),
    url(r'^docs/', include_docs_urls(title='Danesh Boom Documentation')),
    url(r'^dev/', admin.site.urls),
    url('^soc/', include('social_django.urls', namespace='social')),
    url(r'^media/(?P<name>[^/]+)$', media.views.serve, name='media'),
<<<<<<< HEAD
    url(r'^graphql', SafeGraphQLView.as_view(graphiql=True, schema=schema)),

    url(r'^messages/', include('chats.urls', namespace='messages')),

    url(r'^', include('users.urls')),
=======
    url(r'^graphql', SafeGraphQLView.as_view(graphiql=True, schema=schema))
    #url(r'^', include('users.urls')),
>>>>>>> saeid
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
