#!/usr/bin/python
# -*- coding: utf-8 -*-
#import toml
import os
import re
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
    
    text_file = directory+'konkurs.txt'
    call('bash -c "pdf2txt -o {0} -p 34,35 {1} "'.format(text_file,filename), shell=True)
    with open(text_file,'r') as text:
        problems = text.readlines()
    tour_string_num = next(i for i, string in enumerate(problems) if "ТУР" in string)
    problems = problems[tour_string_num+1:]
    while(problems[0].strip()==''):
        problems.pop(0)
    firstnum = int(re.match( r'\d+', problems[0].strip() ).group(0))
    print(firstnum)

    def tour_template(firstnum):
        template = ['tour: {}\n'.format(firstnum//5+1),'  number:\n','  problems:\n']    
        for i in range(firstnum, firstnum+5):
            template.append("""
  - image_art: ''
    image_scheme: ''
    number: {}
    problem: ''
            """.format(i))
        template.append('\n')
        return template
    with open(text_file,'w') as text:        
        text.writelines(tour_template(firstnum))
        text.writelines(problems)


extract('local/2017-10.pdf')