#!/usr/bin/python
# -*- coding: utf-8 -*-
#import toml
import os
import re
import datetime
import itertools
from subprocess import call, check_output

def makedir(d):
        if not os.path.exists(d):
            os.makedirs(d)        

def get_cover(filename):
    directory = 'local/cover/'+os.path.splitext(os.path.basename(filename))[0] + '/'
    makedir(directory)
    print('Extracting cover from PDF file...' )
    call('bash -c "pdftk {0} cat 1 output {1}/01.pdf"'.format(filename,directory), shell=True)
    call('bash -c "convert -density 40 {0}/01.pdf -quality 80 -background white -alpha remove \
     {0}/{1}.jpg"'.format(directory, os.path.splitext(os.path.basename(filename))[0]), shell=True)
    


print('Номер выпуска?')
num=int(input())
#print('local/pdfs/2018-{:0>2}.pdf'.format(num))
get_cover('local/pdfs/2018-{:0>2}.pdf'.format(num))