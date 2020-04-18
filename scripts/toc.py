#!/usr/bin/python
# -*- coding: utf-8 -*-
#import toml
import os
import re
import datetime
import itertools
import yaml
import subprocess
from bs4 import BeautifulSoup   
import common


#def line_type(line):
#    style = line.parent.get('style')
#    if 'Italic' in style:
#      return 'author'
#    if '10px' in style:
#      return 'rubric'
#    if str(line).strip().isdigit():
#      return 'page'
#    else:
#      return 'title'

def lines(pdf):
  html = subprocess.run(['pdf2txt', '-t', 'html', '-p', '3', pdf], stdout=subprocess.PIPE).stdout
  html = html.replace(b'<br/>', b' ')
  soup = BeautifulSoup(html, features="html.parser")
  return [s for s in soup.descendants if not hasattr(s,'text') and s.strip()!='' and position(s)!=None]  
  
def position(line):
    style = line.parent.parent.get('style')
    if type(style)!=str:
        return None
    styles_pairs = [s.strip().split(':') for s in style.split(';')]
    styles_dict = {s[0]:s[1] for s in styles_pairs if len(s)==2}
    if 'top' not in styles_dict.keys() or 'left' not in styles_dict.keys():
        return None
    def get_number(tag):
        s = styles_dict[tag]
        s = [c for c in s if c.isdigit()]
        return int(''.join(s))
    return get_number('top'), get_number('left')
  
def toc(pdf):
  toc = []
  rubric, title, author = '', [], ''
  for l in sorted(lines(pdf),key=position):
    style = l.parent.get('style')
    #print(rubric, title, author)
    if style == None:
      continue
    text = str(l).strip()
    if 'Italic' in style:
      author = text
    elif '10px' in style:
      rubric = text.lower().capitalize()
    elif not text.isdigit():
      title.append(text)
    else:
      page = int(text)
      toc.append({'rubric':rubric, 'title': ' '.join(title), 'page': page, 'author': author})
      title, author = [], ''
      #print('flush ', toc[-1])      
  return sorted(toc, key = lambda t: t['page'])

if __name__ == "__main__":
    num = int(input('Номер выпуска: '))    
    contents = toc(common.pdf(num))
    common.put_table(contents, filename = f'toc-{num}.csv')