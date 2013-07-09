from django.contrib.admin import *
from models import *

# ## -------------------------------------------------------------------------- ##

# class ActivityLabelAdmin(ModelAdmin):
    # list_display = ['name', 'sort_order', 'restriction']

# site.register(ActivityLabel, ActivityLabelAdmin)

# class ActivityAdmin(ModelAdmin):
    # # def copy_activity(self, request, queryset):
        # # for activity in queryset:
            # # activity.copy()
            # # self.message_user(request, 'Copied {0}'.format(activity))
    # # copy_activity.short_description = 'Copy selected activity'
    # # actions = [copy_activity]
    
    # list_display = ['full_title', 'course', 'week', 'weekday']
    # list_filter = ['course', 'activity_label']

# site.register(Activity, ActivityAdmin)

# ## -------------------------------------------------------------------------- ##

# class NullActivityAdmin(ActivityAdmin):
    # def copy_null_activity(self, request, queryset):
        # for null_activity in queryset:
            # null_activity.copy()
            # self.message_user(request, 'Copied {0}'.format(null_activity))
    # copy_null_activity.short_description = 'Copy selected null activity'
    # actions = [copy_null_activity]
    
    # list_display = ['full_title', 'course', 'week', 'weekday']

# site.register(NullActivity, NullActivityAdmin)

# ## -------------------------------------------------------------------------- ##

# class ExerciseProblemAdmin(ModelAdmin):
    # def answered(self, obj):         
        # return (obj.answer != '')
    # answered.boolean = True
    
    # def solved(self, obj):         
        # return (obj.solution != '')
    # solved.boolean = True
    
    # list_display = ['__unicode__', 'answered', 'solved']
    # list_filter = ['source']
    
# site.register(ExerciseSource)
# site.register(ExerciseProblem, ExerciseProblemAdmin)

# class ExerciseTrueFalseAdmin(ModelAdmin):
    # def rationale_given(self, obj):         
        # return (obj.rationale != '')
    # rationale_given.boolean = True
    
    # list_display = ['__unicode__', 'rationale_given']
    
# site.register(ExerciseTrueFalse, ExerciseTrueFalseAdmin)

# # class ExerciseSetProblemInline(TabularInline):
    # # model = ExerciseSetProblem
    # # extra = 0

# class ExerciseSetAdmin(ActivityAdmin):
    # def copy_exercise_set(self, request, queryset):
        # for exercise_set in queryset:
            # exercise_set.copy()
            # self.message_user(request, 'Copied {0}'.format(exercise_set))
    # copy_exercise_set.short_description = 'Copy selected exercise set'
    # actions = [copy_exercise_set]
    
    # def nbr_problems(self, obj):
        # return len(obj.problems.all())
        
    # list_display = ['full_title', 'course', 'week', 'weekday', 'nbr_problems']
    # filter_horizontal = ['problems']
    # # inlines = [ExerciseSetProblemInline]

# site.register(ExerciseSet, ExerciseSetAdmin)

# class ExerciseEquationAdmin(ModelAdmin):
    # pass

# site.register(ExerciseEquation, ExerciseEquationAdmin)

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
