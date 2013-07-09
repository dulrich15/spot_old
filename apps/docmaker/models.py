from django.db import models


# class StudyLecture(NumberedActivity):
    # def get_document_path(self, filename):
        # return posixpath.join('docs', self.course.tag(), filename)
        
    # def get_banner_path(self, filename):
        # return posixpath.join('banners', self.lecture.course.tag(), filename)
    
    # title = CharField(max_length=200)
    # powerpoint = FileField(upload_to=get_document_path, storage=OverwriteStorage(),blank=True)
    # banner = ImageField(upload_to=get_banner_path,storage=OverwriteStorage(),blank=True)
    # examples = ManyToManyField(ExerciseProblem, blank=True)
    # truefalse = ManyToManyField(ExerciseTrueFalse, blank=True)
    # equations = ManyToManyField(ExerciseEquation, blank=True)
    
    # intro = TextField(blank=True)
    # outcomes = TextField(blank=True)
    # summary = TextField(blank=True)
    # credits = TextField(blank=True)

    # scratchpad = TextField(blank=True)
    
    # def documents(self):
        # documents = []
        # documents.append(ActivityDocument(self, 'Slides', 'ls', 0))
        # documents.append(ActivityDocument(self, 'Notes', 'ln', 0))
        # documents.append(ActivityDocument(self, 'Examples', 'lx', 1))
        # return documents

    # def problems(self):
        # # return self.examples
        # return self.examples.exclude(pk__in=self.course.used_exercises())
        
    # def copy(self):
        # lecture = deepcopy(self)
        # lecture.pk = None
        # lecture.id = None
        # lecture.save()
        # lecture.examples = self.examples.all()
        # for s in self.studyslide_set.all():
            # s.pk = None
            # s.lecture = lecture
            # s.save()
              
        
# class StudySlide(Model):
    # def get_slide_path(self, filename):
        # return posixpath.join('slides', self.lecture.course.tag(), filename)
    
    # lecture = ForeignKey(StudyLecture)
    # sort_order = PositiveSmallIntegerField(default=0)

    # title = CharField(max_length=200)
    # image = ImageField(upload_to=get_slide_path,storage=OverwriteStorage(),blank=True)
    
    # notes = TextField(blank=True) # use FileField or FilePathField instead ??
    # examples = ManyToManyField(ExerciseProblem, blank=True)
    # truefalse = ManyToManyField(ExerciseTrueFalse, blank=True)
    # equations = ManyToManyField(ExerciseEquation, blank=True)

    # scratchpad = TextField(blank=True)

    # def __unicode__(self):
        # return self.title    
        
    # class Meta:
        # ordering = ['lecture', 'sort_order']
        
## -------------------------------------------------------------------------- ##
        
# class LabEquipment(Model):
    # item = CharField(max_length=200)
    # location = CharField(max_length=200)
        
    # def __unicode__(self):
        # return u'%s' % self.item
        
    # class Meta:
        # verbose_name_plural = 'lab equipment'
        # ordering = ['item']


# class LabProject(NumberedActivity):
    # title = CharField(max_length=200)
    # worksheet = TextField()
    # notes = TextField(blank=True)
    # equipment = ManyToManyField(LabEquipment, through='LabEquipmentRequest')

    # scratchpad = TextField(blank=True)
    
    # def documents(self):
        # documents = []
        # documents.append(ActivityDocument(self, 'Worksheet', 'lw', 0))
        # documents.append(ActivityDocument(self, 'Equipment Form', 'lf', 2))
        # return documents

    # def copy(self):
        # lab = deepcopy(self)
        # lab.pk = None
        # lab.id = None
        # lab.save()
        # for e in self.labequipmentrequest_set.all():
            # e.pk = None
            # e.lab = lab
            # e.save()
            
                
# class LabEquipmentRequest(Model):
    # lab = ForeignKey(LabProject)
    # equipment = ForeignKey(LabEquipment)
    # quantity = PositiveSmallIntegerField(blank=True,null=True)

    # def __unicode__(self):
        # if self.quantity:
            # return u'%s %s' % (self.quantity, truncate(self.equipment.item))
        # else:
            # return u'%s' % self.equipment.item
            
    # class Meta:
        # ordering = ['equipment__location']
        
## -------------------------------------------------------------------------- ##
        
# class ExerciseSource(Model):
    # title = CharField(max_length=200)
    # author = CharField(max_length=200,blank=True) 

    # def __unicode__(self):
        # return u'%s' % truncate(self.title)
        
        
# class ExerciseProblem(Model):
    # key = SlugField()
    # source = ForeignKey(ExerciseSource)
    
    # question = TextField()
    # answer = TextField()
    # solution = TextField(blank=True)
    # notes = TextField(blank=True)

    # def __unicode__(self):
        # return u'[%s] %s' % (self.key, truncate(self.question))
    
    # class Meta:
        # ordering = ['key']

 
# class ExerciseSet(NumberedActivity):
    # title = CharField(max_length=200, blank=True)
    # problems = ManyToManyField(ExerciseProblem, blank=True)
    # truefalse = ManyToManyField(ExerciseTrueFalse, blank=True)

    # scratchpad = TextField(blank=True)
    
    # def doctag(self):
        # if self.activity_label.name == 'Homework':
            # return 'h'
        # elif self.activity_label.name == 'Quiz':
            # return 'q'
        # else:
            # return 'x'
        
    # def documents(self):
        # documents = []
        # documents.append(ActivityDocument(self, 'Problems', '{}p'.format(self.doctag()), 1))
        # documents.append(ActivityDocument(self, 'Solutions', '{}s'.format(self.doctag()), 1))
        # return documents
        
    # def copy(self):
        # exercise_set = deepcopy(self)
        # exercise_set.pk = None
        # exercise_set.id = None
        # exercise_set.save()
        # exercise_set.problems = self.problems.all()

