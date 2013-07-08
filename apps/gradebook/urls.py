from django.conf.urls.defaults import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^classroom/(\d+)/assignment/$', views.list_assignments, name='list_assignments'),
    url(r'^classroom/(\d+)/assignment/(\d+)/$', views.show_assignment, name='show_assignment'),

    url(r'^classroom/(\d+)/grades/$', views.show_grades, name='show_grades'),
    url(r'^classroom/(\d+)/grades/(\d+)/$', views.show_student, name='show_student'),

    url(r'^classroom/(\d+)/grades/input/$', views.input_grades, name='input_grades'),
    url(r'^classroom/(\d+)/grades/input/(\d+)/$', views.input_grades, name='grade_input'),
    url(r'^classroom/(\d+)/grades/post/(\d+)/$', views.post_grades, name='post_grades'),

#     url(r'^classroom/(\d+)/grades/roster/$', views.show_roster, name='show_roster'),
)