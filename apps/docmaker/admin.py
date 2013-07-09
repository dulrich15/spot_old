from django.contrib.admin import *
from models import *


site.register(ExerciseSource)

class ExerciseProblemAdmin(ModelAdmin):
    def answered(self, obj):         
        return (obj.answer != '')
    answered.boolean = True
    
    def solved(self, obj):         
        return (obj.solution != '')
    solved.boolean = True
    
    list_display = ['__unicode__', 'answered', 'solved']
    list_filter = ['source']
site.register(ExerciseProblem, ExerciseProblemAdmin)

# class ExerciseSetProblemInline(TabularInline):
    # model = ExerciseSetProblem
    # extra = 0

class ExerciseSetAdmin(ModelAdmin):
    def nbr_problems(self, obj):
        return len(obj.problems.all())
        
    list_display = ['__unicode__', 'nbr_problems']
    filter_horizontal = ['problems']
    # inlines = [ExerciseSetProblemInline]
site.register(ExerciseSet, ExerciseSetAdmin)

# ## -------------------------------------------------------------------------- ##

# class StudySlideInline(StackedInline):
    # model = StudySlide
    # extra = 0
    # filter_horizontal = ['examples', 'equations']
    
# class StudyLectureAdmin(ActivityAdmin):
    # def copy_lecture(self, request, queryset):
        # for lecture in queryset:
            # lecture.copy()
            # self.message_user(request, 'Copied {0}'.format(lecture))
    # copy_lecture.short_description = 'Copy selected study lecture'
    # actions = [copy_lecture]
    
    # def nbr_examples(self, obj):         
        # return len(obj.examples.all())
        
    # def nbr_slides(self, obj):         
        # return len(obj.studyslide_set.all())
        
    # list_display = ['full_title', 'course', 'week', 'weekday', 'nbr_examples', 'nbr_slides']
    # filter_horizontal = ['examples']
    # inlines = [StudySlideInline]
    
# site.register(StudyLecture, StudyLectureAdmin)

# class StudySlideAdmin(ModelAdmin):
    # def image_exists(self, obj):
        # try:
            # return os.path.isfile(obj.image.file.name)
        # except:
            # return False
    # image_exists.boolean = True
    
    # def nbr_examples(self, obj):
        # return len(obj.examples.all())
        
    # def nbr_equations(self, obj):
        # return len(obj.examples.all())
        
    # list_filter = ['lecture__course']
    # list_display = ['title', 'image_exists', 'nbr_examples', 'nbr_equations']
    # filter_horizontal = ['examples', 'equations']

# site.register(StudySlide, StudySlideAdmin)


# class StudyJargonAdmin(ModelAdmin):
    # list_display = ['term', 'dfn']

# site.register(StudyJargon, StudyJargonAdmin)

# ## -------------------------------------------------------------------------- ##

# class LabEquipmentRequestInline(TabularInline):
    # model = LabEquipmentRequest
    # extra = 0

# class LabProjectAdmin(ActivityAdmin):
    # def copy_lab(self, request, queryset):
        # for lab in queryset:
            # lab.copy()
            # self.message_user(request, 'Copied {0}'.format(lab))
    # copy_lab.short_description = 'Copy selected lab project'
    # actions = [copy_lab]
    
    # inlines = [LabEquipmentRequestInline]
    
# site.register(LabProject, LabProjectAdmin)

# class LabEquipmentAdmin(ModelAdmin):
    # list_display = ['item', 'location']

# site.register(LabEquipment, LabEquipmentAdmin)

# class LabEquipmentRequestAdmin(ModelAdmin):
    # list_display = ['__unicode__', 'lab']

# site.register(LabEquipmentRequest, LabEquipmentRequestAdmin)
