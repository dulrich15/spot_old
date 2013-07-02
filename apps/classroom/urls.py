from django.conf.urls.defaults import patterns, include, url
from django.views import generic

from . import views

urlpatterns = patterns('',
    url(r'^$', views.list_classrooms, name='list_classrooms'),
    url(r'^(\d+)/$', views.show_classroom, name='show_classroom'),
    url(r'^(\d+)/edit/$', views.edit_classroom, name='edit_classroom'),
    url(r'^(\d+)/post/$', views.post_classroom, name='post_classroom'),
)
