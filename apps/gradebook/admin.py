from django.contrib.admin import *
from models import *


site.register(AssignmentCategory)
site.register(Assignment)
site.register(AssignmentGrade)
site.register(GradeWeight)

class GradeWeightInline(TabularInline):
    model = GradeWeight
    extra = 0

class GradeSchemeAdmin(ModelAdmin):
    inlines = [GradeWeightInline]

site.register(GradeScheme, GradeSchemeAdmin)
