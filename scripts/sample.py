#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import datetime
from subprocess import call, check_call

import csv
import requests

import common

sheets = {2018: 1216387229, 2019: 429063026}

CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTBts-EQ8H1rU283Ur7PG09GYqHwVQB7hnums3gEM6bGeH9DDSJnbrtg8Gv9x5lVTD4oRoFUFWDaKmo/pub?gid={}&single=true&output=csv'.format(sheets[2019])


def get_pages(num):
    with requests.Session() as s:
        content = s.get(CSV_URL).content.decode('utf-8')
        table = list(csv.DictReader(content.splitlines(), delimiter=','))
    articles = [(int(t['Первая страница']), int(t['Всего страниц'])) for t in table if (t['Выпуск']==str(num)) and t['входит в сэмпл?'].strip()=='да']
    pages = [set(range(a[0]+2, a[0]+a[1]+2)) for a in articles]
    pages = {2,3}.union(*pages)
    return sorted(pages)


def make_sample(num, issue_pdf):
    issue_name = os.path.splitext(os.path.basename(issue_pdf))[0]
    directory = 'local/'+issue_name + '/sample/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    pages = [str(i) for i in get_pages(num)]
    print('Страницы pdf-файла, вошедшие в сэмпл:', pages)
    #pages =  ['1', '2', '3', '18', '19', '20', '21', '22', '16',  '34', '35', '36']
    command = 'pdftk {0} cat {1} output {2}{3}_sample.pdf'.format(issue_pdf, ' '.join(pages), directory, issue_name)
    call('bash -c "{}"'.format(command), shell=True)
        
    

if __name__ == "__main__":
    print('Номер выпуска?')
    num=int(input())
    #print('local/pdfs/2018-{:0>2}.pdf'.format(num))
    make_sample(num, common.pdf(num))