from django.conf.urls.defaults import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^classroom/$', views.list_classrooms, name='list_classrooms'),
    url(r'^classroom/(\d+)/$', views.show_classroom, name='show_classroom'),
    url(r'^classroom/(\d+)/schedule/$', views.show_schedule, name='show_schedule'),
    url(r'^classroom/(\d+)/document/$', views.list_documents, name='list_documents'),
    url(r'^classroom/(\d+)/document/([^/]+)$', views.serve_document, name='serve_document'),
    url(r'', include('apps.gradebook.urls')),
)
