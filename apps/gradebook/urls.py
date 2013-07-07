from django.conf.urls.defaults import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^classroom/(\d+)/assignment/$', views.list_assignments, name='list_assignments'),
#     url(r'^classroom/(\d+)/assignment/(\d+)/$', views.show_assignment, name='show_assignment'),

    url(r'^classroom/(\d+)/grades/$', views.show_grades, name='show_grades'),

    url(r'^classroom/(\d+)/grades/students/$', views.list_students, name='list_students'),
#     url(r'^classroom/(\d+)/grades/students/edit/$', views.edit_student_list, name='edit_student_list'),
    url(r'^classroom/(\d+)/grades/students/(\d+)/$', views.show_student, name='show_student'),
#
#     url(r'^courses/(\d+)/grades/edit/$', views.edit_grades, name='edit_grades'),
#     url(r'^courses/(\d+)/grades/edit/(\d+)$', views.edit_grades),
#     url(r'^courses/(\d+)/grades/dump/$', views.dump_grades, name='dump_grades'),
#     url(r'^courses/(\d+)/grades/roster/$', views.show_roster, name='show_roster'),
)