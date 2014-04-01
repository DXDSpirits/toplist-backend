from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'toplist.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

from django.conf import settings
try:
    if settings.LOCAL_SETTINGS:
        from django.conf.urls.static import static
        import mimetypes
        urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
        mimetypes.add_type("image/png", ".png", True)
except:
    pass
