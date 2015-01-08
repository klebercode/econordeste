from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from filebrowser.sites import site

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', 'econordeste.core.views.home', name='home'),
    # url(r'^institucional/', 'canaa.core.views.institutional',
    #     name='institutional'),
    url(r'^contato/', 'econordeste.core.views.contact', name='contact'),
    url(r'^soundcloud/', 'econordeste.core.views.soundcloud',
        name='soundcloud'),

    url(r'^noticias/', include('econordeste.blog.urls', namespace='blog')),

    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # tinymce
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^mce_filebrowser/', include('mce_filebrowser.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# )
