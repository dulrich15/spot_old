from django.contrib.admin import *
from models import *
from apps.classroom.admin import ClassroomAdmin


site.register(AssignmentCategory)
site.register(Assignment)
site.register(AssignmentGrade)
site.register(AssignmentGradeWeight)

class AssignmentGradeWeightInline(TabularInline):
    model = AssignmentGradeWeight
    extra = 0

ClassroomAdmin.inlines = [AssignmentGradeWeightInline]
