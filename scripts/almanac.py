#!/usr/bin/python
# -*- coding: utf-8 -*-
from subprocess import call, check_call
import common

issue = int(input('Введите номер альманаха:\n'))

issues_folder=common.pdfs() # сменить путь к папке, в которой лежат маленькие файлы 2017-07.pdf и т.д.
year = str(2012+(issue-1)//2)
output_folder = f'local/almanac{issue}/' # эта папка будет создана, если нужно, и в ней произойдёт сборка в файл almanac.pdf. Должна быть пустой.
common.clear_folder(output_folder)

table = common.get_table('almanac'+issue)

filler_file = issues_folder+'/../almanacs/alm-12-ed-1.pdf'

for t in table:
  print(t)
  if not t[0].isdigit():
    continue
  for i in [1,2]:
    t[i]=int(t[i])
  if t[2]==0:
    continue
  common.copy_article(issues_folder, year, t[0], t[1], t[2], output_folder, t[7].zfill(3))
  
command = 'pdftk {0}* cat output {0}almanac.pdf'.format(output_folder)
common.bash(command)

