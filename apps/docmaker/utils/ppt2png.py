from __future__ import division
from __future__ import unicode_literals

import os, sys, shutil, re, codecs
import win32com.client

import msoff
import msppt

from PIL import Image

g = globals()
for c in dir(msoff.constants): g[c] = getattr(msoff.constants, c)
for c in dir(msppt.constants): g[c] = getattr(msppt.constants, c)

# See http://www.lqexcel.com/powerpoint.php as PPT reference

pn = os.path.abspath(os.path.dirname(__file__))
if len(sys.argv) == 1:
    fn = raw_input('Export which file? ')
else:
    fn = sys.argv[1]
bn = os.path.splitext(fn)[0]   
fp = os.path.join(pn, fn)

try:
    crop = (sys.argv[2] == 'crop')
except:
    crop = False

if os.path.isdir(bn):
    shutil.rmtree(bn)
os.mkdir(bn)

Application = win32com.client.Dispatch('PowerPoint.Application')
Application.Visible = True

Presentation = Application.Presentations.Open(r'%s' % fp)
tot = Presentation.Slides.Count
titles = []

for Slide in Presentation.Slides:
    nbr = Slide.SlideNumber
    print '{0:03d} of {1:03d}'.format(nbr, tot) + 12*'\b', 
    try:
        title = Slide.Shapes.Title.TextFrame.TextRange.Text
    except:
        title = ''
    titles.append(title)
    
    img = 'Slide{0:03d} -- {1:s}'.format(nbr, title)
    img = 'Slide{0:03d}'.format(nbr, title)
    img = re.sub('[^-a-zA-Z0-9_() ]+', '', img) # slugify
    img += '.png'
    
    # Slide.Export(os.path.join(pn, bn, img), 'png', 800, 600)
    # Slide.Export(os.path.join(pn, bn, img), 'png', 1024, 768)
    Slide.Export(os.path.join(pn, bn, img), 'png', 1028, 771)

    if crop:
        pf = os.path.join(pn, bn, img)
        img = Image.open(pf)
        # box = (0, 120, 800, 600)
        box = (0, 154, 1024, 768)
        img = img.crop(box)  
        # size = (800, 480)
        # img = img.resize(size, Image.ANTIALIAS)
        img.save(pf)
    
f = codecs.open(os.path.join(pn, bn, 'titles.txt'), 'w', 'utf-8')
f.write('\r\n'.join(['{1:03d} : {0:s}'.format(title, titles.index(title) + 1) for title in titles]))
f.close()
    
Application.Quit()