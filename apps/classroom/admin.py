from django.contrib.admin import *
from models import *


site.register(Department)
    
class ClassroomAdmin(ModelAdmin):
    def copy_classroom(self, request, queryset):
        for classroom in queryset:
            classroom.copy_instance()
            self.message_user(request, 'Copied {0}'.format(classroom))
    copy_classroom.short_description = 'Copy selected classroom'

    actions = [copy_classroom]
    
site.register(Classroom, ClassroomAdmin)

class ClassroomUserAdmin(ModelAdmin):
    list_filter = ['classroom']

site.register(Student, ClassroomUserAdmin)
site.register(Instructor, ClassroomUserAdmin)



