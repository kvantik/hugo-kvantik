#!/usr/bin/python
# -*- coding: utf-8 -*-
#import toml
import os
import re
import datetime
import itertools
from subprocess import call, check_output
#import ruamel.yaml as yaml

def makedir(d):
        if not os.path.exists(d):
            os.makedirs(d)        

def to_roman(i):
    return ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'IV', 'V'][i]

def extract(filename, type='math'):
    issue_name = os.path.splitext(os.path.basename(filename))[0]  # example: issue_name = 2018-09 
    directory = 'local/'+issue_name + '/konkurs-'+type+'/'
    makedir(directory)
    if type == 'math':
        konkurs_pages = '-f 34 -l 35'
    else:
        page = int(input('Введите страницу номера, на которой начинается конкурс, согласно нумерации журнала: '))+2
        pages = int(input('Сколько страниц занимает конкурс (обычно 1 или 2)? '))
        konkurs_pages = '-f {0} -l {1}'.format(page, page + pages)        
    print('Extracting images from PDF file...' )
    images = check_output('bash -c "pdfimages {} -list {}"'.format(konkurs_pages, filename), shell=True).split()
    masks = [int(images[i-1]) for i,s in enumerate(images) if s==b'smask'] 
    print(masks)
    call('bash -c "pdfimages {} -png {} {}raw"'.format(konkurs_pages, filename,directory), shell=True)
    raw_file = lambda i : '{0}raw-{1:0>3}.png'.format(directory,i)

    for m in masks:
        #print(i)
        if not os.path.exists(raw_file(m)):
            break
        call('bash -c " composite -compose CopyOpacity {1} {0} {2}"'.format(raw_file(m-1), raw_file(m), directory+""+str(m-1)+'.png'), shell=True)
#        call('bash -c " rm {0} {1}"'.format(raw_file(i), raw_file(i+1)), shell=True)
    
    text_file = directory+'tour.yaml'
    call('bash -c "touch {}"'.format(text_file), shell=True)
    if type == 'math':
        call('bash -c "pdf2txt -o {0} -p 34,35 {1} "'.format(text_file,filename), shell=True)
    else:
        if pages == 1:
            call('bash -c "pdf2txt -o {} -p {} {} "'.format(text_file, page, filename), shell=True)
        else:
            call('bash -c "pdf2txt -o {} -p {},{} {} "'.format(text_file, page, page+1, filename), shell=True)        
    with open(text_file,'r') as text:
        problems = text.readlines()
    if type == 'math':
        tour_string_num = next(i for i, string in enumerate(problems) if ("ТУР" in string))
    else:
        tour_string_num = [i for i, string in enumerate(problems) if ("ТУР" in string.strip())][0]
    print(problems[tour_string_num])
    problems = problems[tour_string_num+1:]
    while(bool(re.search(r'\d', problems[0]))==False):
        problems.pop(0)
    print(problems)
    firstnum = int(re.match( r'\d+', problems[0].strip() ).group(0))
    print(firstnum)

    
    template = ['tour:\n',
                    '  number: {}\n'.format(firstnum//5+1),
                    '  title: {} тур\n'.format(to_roman(firstnum//5+1)),
                    '  deadline: 1\n',
                    '  problems:\n']    
    for i in range(firstnum, firstnum+5):
            template.append("""
  - author:
    image_art: {0}.png
    image_scheme: ''
    number: {0}
    problem: ''
            """.format(i))
    template.append('\n')

    with open(text_file,'w') as text:        
        text.writelines(template)
        text.writelines(problems)

if __name__ == "__main__":
    print('Номер выпуска?')
    num=int(input())
    type = input('Тип конкурса (ввод для math): ')
    if type =='':
        type ='math'
    #print('local/pdfs/2018-{:0>2}.pdf'.format(num))
    extract('local/pdfs/2019-{:0>2}.pdf'.format(num), type=type)