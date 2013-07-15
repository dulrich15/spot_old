import fnmatch
import os

def get_choices_from_list(mylist):
    choices = []
    for x in mylist:
        choices += [(len(choices), x)]
    return choices

def get_choices_from_path(mypath, filter='*'):
    choices = []
    for f in os.listdir(mypath):
        if fnmatch.fnmatch(f, filter):
            choices += [(f, f)]
    return choices

weekday_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
weekday_choices = get_choices_from_list(weekday_list)

access_list = ['Public', 'Student', 'Instructor']
access_choices = get_choices_from_list(access_list)

