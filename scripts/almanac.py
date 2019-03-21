#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import datetime
from subprocess import call, check_call

import csv
import requests

import common

issue = int(input('Введите номер альманаха:\n'))

sheets = {12: 936711077, 13: 990127193, 14: 1725308277}

CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTBts-EQ8H1rU283Ur7PG09GYqHwVQB7hnums3gEM6bGeH9DDSJnbrtg8Gv9x5lVTD4oRoFUFWDaKmo/pub?gid={}&single=true&output=csv'.format(sheets[issue])
issues_folder=common.pdfs() # сменить путь к папке, в которой лежат маленькие файлы 2017-07.pdf и т.д.
year = str(2012+(issue-1)//2)
output_folder='local/almanac{}/'.format(issue) # эта папка будет создана, если нужно, и в ней произойдёт сборка в файл almanac.pdf. Должна быть пустой.
#print(issue, CSV_URL, year, output_folder)
#exit()

if not os.path.exists(output_folder):
            os.makedirs(output_folder)  

if len(os.listdir(output_folder)) > 0: # если папка не пуста - удалить из неё все файлы
  input("Папка {} будет очищена. Нажмите Enter для продолжения (ctrl+c для выхода)".format(output_folder))
  call('bash -c "rm {}*"'.format(output_folder), shell=True)

csv_file = input("Введите имя файла таблицы (в csv, ввод для гугл-таблицы): ")
if csv_file == '':
  with requests.Session() as s:
    content = s.get(CSV_URL).content.decode('utf-8')
    
else:
  with open(csv_file, 'r', encoding='utf8') as f:
    content = f.read()
table = list(csv.reader(content.splitlines(), delimiter=','))

filler_file = issues_folder+'/../almanacs/alm-12-ed-1.pdf'

for t in table:
  print(t)
  if not t[0].isdigit():
    continue
  for i in [1,2]:
    t[i]=int(t[i])
  if t[2]==0:
    continue
  command = 'pdftk {0}.pdf cat {1}-{2} output {3}.pdf'.format(issues_folder+year+'-'+t[0].zfill(2), t[1]+2, t[1]+1+t[2], output_folder+t[7].zfill(3))
  print(command)
  call('bash -c "{}"'.format(command), shell=True)
  
command = 'pdftk {0}* cat output {0}almanac.pdf'.format(output_folder)
call('bash -c "{}"'.format(command), shell=True)
