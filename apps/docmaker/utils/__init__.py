# from __future__ import division
# from __future__ import unicode_literals


# def make_pdf(latex):    
    
    # curdir = os.getcwd()
    # os.chdir(app.config['TEMPDIR_LATEX'])

    # basename = 'temp'
    
    # texname = '%s.tex' % basename
    # idxname = '%s.idx' % basename
    # pdfname = '%s.pdf' % basename

    # texfile = codecs.open(texname, 'w', 'utf-8')
    # texfile.write(latex)
    # texfile.close()

    # # try:
        # # for ext in ['idx','ind','ilg','aux','log','out','toc','tex','pdf','png']:
            # # os.remove('%s.%s' % (basename, ext))
    # # except:
        # # pass

    # for i in range(3):
        # cmd = os.path.join(app.config['TEX_PATH'], 'pdflatex')
        # cmd = [cmd, '--interaction=nonstopmode', texname]
        # p = Popen(cmd,stdout=PIPE,stderr=PIPE)
        # out, err = p.communicate()

    # try:
        # open(idxname)
        # if os.path.getsize(idxname):

            # cmd = os.path.join(app.config['TEX_PATH'], 'makeindex')
            # cmd = [cmd,  idxname]
            # p = Popen(cmd, stdout=PIPE, stderr=PIPE)
            # out, err = p.communicate()

            # cmd = os.path.join(app.config['TEX_PATH'], 'pdflatex')
            # cmd = [cmd, '--interaction=nonstopmode', texname]
            # p = Popen(cmd, stdout=PIPE, stderr=PIPE)
            # out, err = p.communicate()
    # except:
        # pass

    # os.chdir(curdir)

    # return os.path.join(app.config['TEMPDIR_LATEX'], pdfname)


# def docmaker(filename):
    # document = Document.documents[filename]
    # activity = document.activity
    # event = activity.event

    # context = dict()

    # if not activity.keys:
        # flash("No keys found -- Nothing built :(")
        # return False
    # else:
    
        # keys = activity.keys
        # if activity.category.lower() in ('quiz', 'exam') and document.filetype.lower() in ('problems', 'solutions'):
            # if document.filetype.lower() == 'solutions':
                # show = {'answers': True, 'solutions': True}
            # else:
                # show = {'answers': False, 'solutions': False}
                
            # db = get_db()
            # sql = '''
                # SELECT * 
                # FROM courses_exerciseproblem 
                # WHERE key IN ({})
            # '''
            # sql = sql.format('"' + '","'.join(keys) + '"')
            # problems = db.execute(sql).fetchall()

            # context['problems'] = problems
            # context['show'] = show
            
            # template = 'qz.tex'
            
        # elif activity.category.lower() == 'homework' and document.filetype.lower() in ('problems', 'solutions'):
            # if document.filetype.lower() == 'solutions':
                # show = {'answers': True, 'solutions': True}
            # else:
                # show = {'answers': True, 'solutions': False}
                
            # db = get_db()
            # sql = '''
                # SELECT * 
                # FROM courses_exerciseproblem 
                # WHERE key IN ({})
            # '''
            # sql = sql.format('"' + '","'.join(keys) + '"')
            # problems = db.execute(sql).fetchall()

            # context['problems'] = problems
            # context['show'] = show
            
            # template = 'hw.tex'
                
        # elif activity.category.lower() == 'lecture' and document.filetype.lower() == 'notes':
                
            # if len(keys) > 1:
                # flash("Why is there more than one key for {}?".format(activity.label))
                # return False
            
            # db = get_db()
            # sql = '''
                # SELECT
                    # activity_ptr_id AS key,
                    # title,
                    # intro                    
                # FROM courses_studylecture 
                # WHERE activity_ptr_id IN ({})
            # '''
            # sql = sql.format('"' + '","'.join(keys) + '"')
            # row = db.execute(sql).fetchone()
            # lecture = StudyLecture(**row)

            # sql = '''
                # SELECT * 
                # FROM courses_studyslide 
                # WHERE lecture_id IN ({})
            # '''
            # sql = sql.format('"' + '","'.join(keys) + '"')
            # rows = db.execute(sql).fetchall()

            # slides = list()
            # for row in rows:
                # slide = dict(zip(row.keys(), row))
                # slide['image'] = slide['image'].rsplit('/', 1)[1]
                # slide['image_path'] = os.path.join(course.lib, 'slides', slide['image'])
                # slide['image_url'] = '/slide/{}'.format(slide['image'])
                # slides.append(slide)

            # lecture.slides = slides

            # context['lecture'] = lecture
            
            # template = 'ln.tex'
                
        # elif activity.category.lower() == 'lab' and document.filetype.lower() in ('worksheet', 'equipment'):
                
            # if len(keys) > 1:
                # flash("Why is there more than one key for {}?".format(activity.label))
                # return False
            
            # db = get_db()
            # sql = '''
                # SELECT * 
                # FROM courses_labproject 
                # WHERE activity_ptr_id IN ({})
            # '''
            # sql = sql.format('"' + '","'.join(keys) + '"')
            # row = db.execute(sql).fetchone()
            # lab = dict(zip(row.keys(), row))

            # lab['key'] = keys[0]

            # sql = '''
                # SELECT * 
                # FROM courses_labequipmentrequest AS a
                # INNER JOIN courses_labequipment AS b
                # ON a.equipment_id = b.id
                # WHERE a.lab_id IN ({})
            # '''
            # sql = sql.format('"' + '","'.join(keys) + '"')
            # rows = db.execute(sql).fetchall()

            # equipment = list()
            # for row in rows:
                # x = dict(zip(row.keys(), row))
                # equipment.append(x)

            # lab['equipment'] = equipment

            # context['lab'] = lab            
            # if document.filetype.lower() == 'equipment':
                # template = 'lf.tex'
            # else:
                # template = 'lb.tex'
                
        # else:
        
            # flash("I don't know how to build {} yet :(".format(filename))
            # return False
            
        # context['course'] = course
        # context['event'] = event
        # context['activity'] = activity
        # context['document'] = document
        
        # latex = render_template(template, **context)
        
        # pdfpath = make_pdf(latex)
        # docpath = os.path.join(course.lib, 'docs', filename)
        # shutil.move(pdfpath, docpath) # this will overwrite
        
        # print 'Just created {}'.format(docpath)
    