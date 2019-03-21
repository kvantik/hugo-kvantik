#!/usr/bin/python
# -*- coding: utf-8 -*-
#import toml
import os
import re
import datetime
import itertools
#import ruamel.yaml as yaml

import common

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
        pages = [34, 35]
    else:
        page = int(input('Введите страницу номера, на которой начинается конкурс, согласно нумерации журнала: '))+2
        pages =  range(page, page + int(input('Сколько страниц занимает конкурс (обычно 1 или 2)? ')))        
    
    common.pdf2images(filename, directory, pages)
    
    problems = common.pdf2txt(filename, pages)
    print(problems)
    tour_string_num = [i for i, string in enumerate(problems) if ("ТУР" in string.strip())][0]
    print(problems[tour_string_num])
    problems = problems[tour_string_num+1:]
    while(bool(re.search(r'\d', problems[0]))==False):
        problems.pop(0)
    print(problems)
    firstnum = int(re.match( r'\d+', problems[0].strip() ).group(0))
    print(firstnum)
    tour = firstnum//5+1

    
    template = ['tour:\n',
                    '  number: {}\n'.format(tour),
                    '  title: {} тур\n'.format(to_roman(tour)),
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

    with open(directory+str(tour)+'.yaml','w') as text:        
        text.writelines(template)
        text.writelines(problems)

if __name__ == "__main__":
    print('Номер выпуска?')
    num=int(input())
    type = input('Тип конкурса (ввод для math): ')
    if type =='':
        type ='math'
    #print('local/pdfs/2018-{:0>2}.pdf'.format(num))
    extract(common.pdf(num), type=type)