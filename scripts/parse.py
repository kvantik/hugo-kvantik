#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import datetime
import itertools
import yaml
import subprocess
from bs4 import BeautifulSoup   
import common


def parse(pdf):
  html = subprocess.run(['pdf2txt', '-t', 'html', '-p', '3', pdf], stdout=subprocess.PIPE).stdout
  html = html.replace(b'<br/>', b' ')
  soup = BeautifulSoup(html, features="html.parser")
  return soup, [s for s in soup.descendants if not hasattr(s,'text') and s.strip()!='']  

  
if __name__ == "__main__":
    num = int(input('Номер выпуска: '))    
    soup, nodes = parse(common.pdf(num))
