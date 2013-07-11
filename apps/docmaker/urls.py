from django.conf.urls.defaults import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^classroom/(\d+)/docmakers/$', views.list_docmakers, name='list_docmakers'),
    url(r'^classroom/(\d+)/docmakers/build/$', views.run_docmaker, name='run_docmaker'),
)