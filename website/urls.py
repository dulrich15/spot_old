from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.simple import direct_to_template
# from django.views.generic.simple import redirect_to

from . import views

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', direct_to_template, {
        'template'      : 'website/index.html',
        'extra_context' : { 'apps' : ('admin',) + settings.MY_APPS }
    }),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
)

for app in settings.MY_APPS:
    urlpatterns += patterns('', url(r'', include('apps.{}.urls'.format(app))),)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
