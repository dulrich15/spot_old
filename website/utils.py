import fnmatch
import os

def get_choices_from_list(mylist):
    choices = []
    for x in mylist:
        choices += [(len(choices), x)]
    return choices

def get_choices_from_path(mypath, filter='*'):
    choices = []
    for dirpath, dirnames, filenames in os.walk(mypath):
        for f in filenames:
            filepath = os.path.join(dirpath, f)
            filename = filepath.replace(mypath, '')[1:]
            filename = '/'.join(filename.split(os.path.sep))
            if fnmatch.fnmatch(filename, filter):
                choices += [(filename, filename)]
    return choices

weekday_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
weekday_choices = get_choices_from_list(weekday_list)

access_list = ['Public', 'Student', 'Instructor']
access_choices = get_choices_from_list(access_list)

