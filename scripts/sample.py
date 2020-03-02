#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Kvantik sample pdf generator.

Usage:
  sample.py [--issue=<n>] [--pages=<pagelist>]

Options:
  -h --help     Show this screen.
  --issue=<n>   Issue number.
  --pages=<pagelist> List of pages [default: 'from table']
"""
from docopt import docopt

import os
import datetime
from subprocess import call, check_call

import csv
import requests
import common
import re



def get_pages(num):
    with requests.Session() as s:
        content = s.get(common.sheet_url(common.year)).content.decode('utf-8')
        table = list(csv.DictReader(content.splitlines(), delimiter=','))
    articles = [(int(t['Первая страница']), int(t['Всего страниц'])) for t in table if (t['Выпуск']==str(num)) and t['входит в сэмпл?'].strip()=='да']
    pages = [set(range(a[0]+2, a[0]+a[1]+2)) for a in articles]
    pages = {2,3}.union(*pages)
    return sorted(pages)


def make_sample(num, issue_pdf, pages=None):
    issue_name = os.path.splitext(os.path.basename(issue_pdf))[0]
    directory = 'local/'+issue_name + '/sample/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    if pages == None:
        pages = [str(i) for i in get_pages(num)]
    print('Страницы pdf-файла, вошедшие в сэмпл:', pages)
    #pages =  ['1', '2', '3', '18', '19', '20', '21', '22', '16',  '34', '35', '36']
    command = 'pdftk {0} cat {1} output {2}{3}_sample.pdf'.format(issue_pdf, ' '.join(pages), directory, issue_name)
    call('bash -c "{}"'.format(command), shell=True)
        
    

if __name__ == "__main__":
    arguments = docopt(__doc__)
    print(arguments)
    pages = [number for number in re.findall('\d+',arguments['--pages'])] if arguments['--pages']!=None else None
    print('Номер выпуска?')
    num=int(input()) if arguments['--issue']==None else int(arguments['--issue'])
    #print('local/pdfs/2018-{:0>2}.pdf'.format(num))
    make_sample(num, common.pdf(num), pages)