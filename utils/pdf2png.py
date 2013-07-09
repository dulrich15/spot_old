from __future__ import division
from __future__ import unicode_literals

import os, sys, shutil, re, codecs
from subprocess import Popen, PIPE 
from PIL import Image

# GS_CMD = r'C:\Program Files\my\apps\Ghostscript\bin\gswin32c.exe'
GS_CMD = r'/usr/bin/gs'

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

cmd = [GS_CMD,
    '-q',
    '-dBATCH',
    '-dNOPAUSE',
    '-sDEVICE=png16m',
    '-r204',
    '-dTextAlphaBits=4',
    '-dGraphicsAlphaBits=4',
#    r'-sOutputFile={}\Slide%03d.png'.format(bn),
    r'-sOutputFile={}/Slide%03d.png'.format(bn),
    fn,
    ]

if os.path.isdir(bn):
    shutil.rmtree(bn)
os.mkdir(bn)

p = Popen(cmd,stdout=PIPE,stderr=PIPE)
out, err = p.communicate()

if crop:
    print "Cropping..."
    for i in range(99):
        nbr = i + 1

        fn = 'Slide{0:03d}.png'.format(nbr)
        pf = os.path.join(pn, bn, fn)
        img = Image.open(pf)
        box = (2, 119, 1026, 733)
#        box = (0, 154, 1024, 768)
        img = img.crop(box)  
        img.save(pf)

