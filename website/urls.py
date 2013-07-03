from django.conf import settings
from django.conf.urls import patterns, include, url
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

    url(r'', include('apps.classroom.urls')),
)

