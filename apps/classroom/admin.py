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

class DocumentAdmin(ModelAdmin):
    list_filter = ['classroom']
    list_display = ['__unicode__', 'access', 'classroom']

site.register(Document, DocumentAdmin)

site.register(Extension)
site.register(Textbook)

class PageDivAdmin(ModelAdmin):
    list_filter = ['classroom']
    list_display = ['title', 'access', 'sort_order', 'classroom']

site.register(PageDiv, PageDivAdmin)


## split below to separate app??


class ActivityInline(StackedInline):
    model = Activity
    extra = 0
    filter_horizontal = ['documents']

class ActivityBlockAdmin(ModelAdmin):
    def nbr_activities(self, obj):
        return len(obj.activities.all())

    list_filter = ['classroom']
    list_display = ['__unicode__', 'nbr_activities', 'classroom']
    inlines = [ActivityInline]

site.register(ActivityBlock, ActivityBlockAdmin)

class ActivityTypeAdmin(ModelAdmin):
    list_display = ['__unicode__', 'sort_order']

site.register(ActivityType, ActivityTypeAdmin)

class ActivityAdmin(ModelAdmin):
    def nbr_documents(self, obj):
        return len(obj.documents.all())

    list_filter = ['classroom']
    list_display = ['__unicode__', 'nbr_documents', 'classroom']
    filter_horizontal = ['documents']

site.register(Activity, ActivityAdmin)
