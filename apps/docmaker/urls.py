from django.conf.urls.defaults import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^classroom/(\d+)/docmaker/$', views.list_docmakers, name='list_docmakers'),
)