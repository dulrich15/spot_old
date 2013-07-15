import os

def get_choices_from_list(mylist):
    choices = []
    for x in mylist:
        choices += [(len(choices), x)]
    return choices

def get_choices_from_path(mypath):
    choices = []
    for f in os.listdir(mypath):
        if os.path.isfile(os.path.join(mypath, f)):
            choices += [(f, f)]
    return choices


