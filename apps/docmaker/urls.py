from django.conf.urls.defaults import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^classroom/(\d+)/docmakers/$', views.list_docmakers, name='list_docmakers'),
    url(r'^classroom/(\d+)/docmakers/build/(\d+)/(\d+)/$', views.build_document, name='build_document'),
    url(r'^classroom/(\d+)/docmakers/build/all/$', views.build_all, name='build_all'),
)