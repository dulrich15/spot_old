from django.contrib.admin import *
from models import *


site.register(Department)
site.register(ActivityType)
    

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


class ActivityBlockAdmin(ModelAdmin):
    def nbr_activities(self, obj):
        return len(obj.activities.all())

    list_filter = ['classroom']
    list_display = ['__unicode__', 'classroom', 'nbr_activities']
    filter_vertical = ['activities']
site.register(ActivityBlock, ActivityBlockAdmin)


class ActivityAdmin(ModelAdmin):
    def nbr_documents(self, obj):
        return len(obj.documents.all())

    list_filter = ['classroom']
    list_display = ['__unicode__', 'classroom', 'nbr_documents']
    filter_vertical = ['documents']
site.register(Activity, ActivityAdmin)


class DocumentAdmin(ModelAdmin):
    list_filter = ['classroom']
    list_display = ['__unicode__', 'classroom', 'access']

site.register(Document, DocumentAdmin)



