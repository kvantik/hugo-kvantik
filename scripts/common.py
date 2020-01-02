from subprocess import call, check_output
import os
from functools import lru_cache
import re
import csv
import requests

repo_root = '../'  
year = 2020


@lru_cache()
def pdfs():
    default = '../../small-pdfs/issues/'
    pdfs = input("Введите путь к папке с маленькими файлами журнала (Enter для {}):".format(default))
    if pdfs == '':
      pdfs = default
    if pdfs[-1]!= '/':
      pdfs = pdfs + '/'
    return pdfs
     
     

def pdf(num=None, year=year):
  if num == None:
    num = int(input('Номер выпуска: '))
  return '{0}{1}-{2:02}.pdf'.format(pdfs(), year, num)
  
  
def pdf2images(filename, output_dir, pages):
    print('Extracting images from PDF file...' )
    konkurs_pages = '-f {0} -l {1}'.format(min(pages),max(pages))
    #print(pages)
    images = check_output('bash -c "pdfimages {0} -list {1}"'.format(konkurs_pages, filename), shell=True).split()
    masks = [int(images[i-1]) for i,s in enumerate(images) if s==b'smask'] 
    print(masks)
    call('bash -c "pdfimages {} -png {} {}raw"'.format(konkurs_pages, filename,output_dir), shell=True)
    raw_file = lambda i : '{0}raw-{1:0>3}.png'.format(output_dir,i)

    for m in masks:
        #print(i)
        if not os.path.exists(raw_file(m)):
            break
        call('bash -c " composite -compose CopyOpacity {1} {0} {2}"'.format(raw_file(m-1), raw_file(m), output_dir+""+str(m-1)+'.png'), shell=True)
#        call('bash -c " rm {0} {1}"'.format(raw_file(i), raw_file(i+1)), shell=True)
    
    

def pdf2txt(filename, pages):
    return check_output('bash -c "pdf2txt -p {0} {1} "'.format(','.join(str(p) for p in pages),filename), shell=True).decode('utf8').split('\n')
    



def sheet_url(sheet):
  if type(sheet)==int:
    sheet_id = {
      2012: 640477208,
      2013: 1675122960,
      2014: 1893976624,
      2015: 155630517,
      2016: 1051356883,
      2017: 2108776824,
      2018: 1216387229, 
      2019: 429063026,
      2020: 589627342,
      }[sheet]
  elif sheet.lower().startswith('alm'):
    alm_num = re.findall(r'\d+',sheet)[0]
    sheet_id = {
      12: 936711077, 
      13: 990127193, 
      14: 1725308277,
      15: 2135853335,
      }[int(alm_num)]
  else:
    raise ValueError
  return f'https://docs.google.com/spreadsheets/d/e/2PACX-1vTBts-EQ8H1rU283Ur7PG09GYqHwVQB7hnums3gEM6bGeH9DDSJnbrtg8Gv9x5lVTD4oRoFUFWDaKmo/pub?gid={sheet_id}&single=true&output=csv'


def get_table(sheet, gsheet=False):
  if not gsheet:
    csv_file = input(f"Введите имя файла таблицы {sheet} (в csv, ввод для гугл-таблицы): ")
    gsheet = csv_file == ''
  if gsheet:
    with requests.Session() as s:
      content = s.get(sheet_url(sheet)).content.decode('utf-8')
  else:
    with open(csv_file, 'r', encoding='utf8') as f:
      content = f.read()
  content = content.splitlines()
  headers = content[0].split(',')
  headers = [h.lower().split(' ')[0] for h in headers]
  content[0] = ','.join(headers)
  return [dict(d) for d in csv.DictReader(content, delimiter=',')]


def bash(command):
  print(command)
  call(f'bash -c "{command}"', shell=True)

def clear_folder(folder):
  if not os.path.exists(folder):
    os.makedirs(folder)  
  if len(os.listdir(folder)) > 0: # если папка не пуста - удалить из неё все файлы
    input(f"Папка {folder} будет очищена. Нажмите Enter для продолжения (ctrl+c для выхода)")
    bash(f"rm {folder}*")

def copy_article(issues_folder, year, issue, firstpage, pages, output_folder, output_name):
  input_file = f'{issues_folder}{year}-{str(issue).zfill(2)}.pdf'
  output_file = f'{output_folder}{output_name}.pdf'
  page_range = f'{int(firstpage)+2}-{int(firstpage)+int(pages)+1}'
  command = f'pdftk {input_file} cat {page_range} output {output_file}'
  bash(command)


