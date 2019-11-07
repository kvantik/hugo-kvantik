#!/usr/bin/python
# -*- coding: utf-8 -*-
#import toml
import os
import re
import datetime
import itertools
import yaml

import common

def get_directory(filename, kind):
    issue_name = os.path.splitext(os.path.basename(filename))[0]  # example: issue_name = 2018-09 
    directory = 'local/'+issue_name + '/konkurs-'+kind+'/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def to_roman(i):
    return ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'IV', 'V'][i]

    
def get_authors(lines, kind="math"):
    if kind!="math":
        return dict()
    line_num = [i for i, string in enumerate(lines) if ("Авторы:" in string.strip())][0]
    authors_line = lines[line_num][7:]
    while (bool(re.search(r'\(\d+\)', lines[line_num+1]))==True):
        line_num+=1
        authors_line += lines[line_num]
    author_lines = authors_line.split(')')
    authors = {}
    for a in author_lines:
        if '(' not in a:
            continue
        author, nums = a.split('(')
        for num in re.findall(r'\d+', nums):
            authors[int(num)] = author.strip(' ,')
    return authors
    
def get_pages(kind):    
    if kind == 'math':
        return [34, 35]
    else:
        page = int(input('Введите страницу номера, на которой начинается конкурс, согласно нумерации журнала: '))+2
        return range(page, page + int(input('Сколько страниц занимает конкурс (обычно 1 или 2)? ')))        

        
def get_problem(lines, num):    
    problem = [s for s in enumerate(lines) if ("{}.".format(num) in string.strip())][0]
    

def skip_until(lines, token):
    res = ''
    while len(lines)!=0 and (token not in lines[0]):
        res += lines[0].strip("\n")
        lines.pop(0)
    return res
       
def parse_tour(lines, kind="math"):
    skip_until(lines, "ТУР")
    authors = get_authors(lines, kind=kind)
    print(lines)
    firstnum = int(re.match( r'\d+', next(x for x in lines if bool(re.search(r'\d+.', x))==True)  ).group(0))
    print("Номер первой задачи:", firstnum)
    skip_until(lines, '{}.'.format(firstnum))
    firstnum = int(re.match( r'\d+.', lines[0].strip() ).group(0)[:-1])
    problems = []
    for i in range(firstnum, firstnum+5):
        problems.append({
            "problem": skip_until(lines, '{}.'.format(i+1))[3:].strip(),
            "author": authors[i] if i in authors.keys() else "",
            "image_art": "{}.png".format(i),
            "image_scheme": "",
            "number": i,
        })
        
    tour_num = firstnum//5+1
    return {"tour":{
        "number" : tour_num, 
        "title": '{} тур'.format(to_roman(tour_num)),
        "deadline": '1 (месяц?)',
        "problems": problems
        }}

        
def extract(filename, kind='math'):
    directory = get_directory(filename, kind)
    pages = get_pages(kind)    
    common.pdf2images(filename, directory, pages)    
    problems = common.pdf2txt(filename, pages)
    print(problems)
    lines = problems[:]

    # old generation start
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
                    '  deadline: 1 (месяц?)\n',
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

    with open(directory+str(tour)+'.old.yaml','w') as text:        
        text.writelines(template)
        text.writelines(problems)
    # old generation stop

    with open(directory+str(tour)+'.yaml','w') as text:        
        text.writelines(yaml.dump(parse_tour(lines, kind=kind), allow_unicode=True, default_flow_style=False, width = 10000))

if __name__ == "__main__":
    num=int(input('Номер выпуска: '))
    kind = input('Тип конкурса (ввод для math): ')
    if kind =='':
        kind ='math'
    extract(common.pdf(num), kind=kind)