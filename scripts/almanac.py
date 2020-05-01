#!/usr/bin/python
# -*- coding: utf-8 -*-
from subprocess import call, check_call
import common

issue = int(input('Введите номер альманаха:\n'))

issues_folder=common.pdfs() # сменить путь к папке, в которой лежат маленькие файлы 2017-07.pdf и т.д.
year = str(2012+(issue-1)//2)
output_folder = f'local/almanac{issue}/' # эта папка будет создана, если нужно, и в ней произойдёт сборка в файл almanac.pdf. Должна быть пустой.
common.clear_folder(output_folder)

table = common.get_table('almanac'+str(issue))

filler_file = issues_folder+'/../almanacs/alm-12-ed-1.pdf'


if issue == 15:
    with open('alm15-ia.txt', 'r') as file:
        ia_order = [line.strip('\n').split('\t') for line in file.readlines()]
    new_table = []
    page = 6
    for ia in ia_order:
        candidates = [t for t in table if t['выпуск']==ia[0] and t['первая']==ia[1]]
        if len(candidates)==1:
            new_table.append(candidates[0])
            new_table[-1]['страница']=page
            page += int(new_table[-1]['всего'])
        else:
            print(f'Error, candidates for {ia} are {candidates}')
    for t in table:
        candidates = [nt for nt in new_table if t['выпуск']==nt['выпуск'] and t['первая']==nt['первая']]
        if len(candidates)==0:
            print(f'lost item {t}')
    table = new_table
    
    
for t in table:
  print(t)
  if not t['выпуск'].isdigit():
    continue
  common.copy_article(issues_folder, year, int(t['выпуск']), int(t['первая']), int(t['всего']), output_folder, str(t['страница']).zfill(3))
  
command = 'pdftk {0}* cat output {0}almanac.pdf'.format(output_folder)
common.bash(command)

