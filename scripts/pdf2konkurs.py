#!/usr/bin/python
# -*- coding: utf-8 -*-
#import toml
import os
import datetime
import itertools
from subprocess import call, check_call
import ruamel.yaml as yaml

def makedir(d):
        if not os.path.exists(d):
            os.makedirs(d)        

def extract(filename):
    directory = 'local/konkurs/'+os.path.splitext(os.path.basename(filename))[0] + '/'
    makedir(directory)
    print('Extracting images from PDF file...' )
    call('bash -c "pdfimages -f 34 -l 35 -list {0}"'.format(filename), shell=True)
    call('bash -c "pdfimages -f 34 -l 35 -png {0} {1}raw"'.format(filename,directory), shell=True)

    raw_file = lambda i : '{0}raw-{1:0>3}.png'.format(directory,i)
    for i in itertools.count(0,2):
        print(i)
        if not os.path.exists(raw_file(i)):
            break
        call('bash -c " composite -compose CopyOpacity {1} {0} {2}"'.format(raw_file(i), raw_file(i+1), directory+""+str(i//2)+'.png'), shell=True)
        call('bash -c " rm {0} {1}"'.format(raw_file(i), raw_file(i+1)), shell=True)


extract('local/2017-10.pdf')