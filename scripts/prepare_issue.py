#!/usr/bin/python
# -*- coding: utf-8 -*-
#import toml
import os
import datetime
import pygsheets
from subprocess import call, check_call
import ruamel.yaml as yaml

def makedir(d):
        if not os.path.exists(d):
            os.makedirs(d)        

def article2md(a):
    if a == None:
         return
    a['date'] = datetime.datetime.now().isoformat('T')[:-7]+'+03:00'
    dir_path = 'local/gsheets2article/'+a['year']+'/'+a['month']+'/'
    directory = os.path.dirname(dir_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(dir_path+str(a['first_page'])+'.md', 'w', encoding = "utf-8") as output:
        #output.write('+++\n')
        #output.writelines(toml.dumps(a))
        #output.write('+++\n')
        output.write('---\n')
        output.writelines(yaml.dump(i, allow_unicode=True, width=120))
        output.write('---\n')

def pdf2jpg(filename, pages=None):
    if not os.path.exists(filename):
        print('non-existent file ', filename)
        return
#    path, file = os.path.split(filename)
    directory = 'local/jpeg/'+os.path.splitext(os.path.basename(filename))[0] + '/'
    makedir(directory)
    makedir(directory + 'thumbnails')
    makedir(directory + 'gallery')
    print('  Splitting PDF file to pages...' )
    call('bash -c "pdftk {0} burst output {1}/%02d.pdf"'.format(filename,directory), shell=True)
    print('  Converting pages to JPEG files...')
    call('bash -c "convert -density 40 {0}/01.pdf -quality 80 -background white -alpha remove \
     {0}/cover.jpg"'.format(directory), shell=True)
    if pages == None:
        pages = range(1,37)
    for i in pages:
        call('bash -c "convert  -density 200 {0}/{1}.pdf -quality 90 -background white -alpha remove \
            {0}/gallery/{1}.jpg"'.format(directory, str(i).zfill(2)), shell=True)
        call('bash -c "convert -density 20 {0}/{1}.pdf -quality 80 -background white -alpha remove \
            {0}/thumbnails/{1}.jpg"'.format(directory, str(i).zfill(2)), shell=True)
    call('bash -c "rm {}*.pdf"'.format(directory), shell=True)
    call('bash -c "rm {}doc_data.txt"'.format(directory), shell=True)
    print("pdf2jpg done for "+filename)

def issue2md(year, month, slogans):
    i = {
          'year' : str(year),
          'month' : str(month).zfill(2),
          'orphan_slogans' : slogans,
          'date' : datetime.datetime.now().isoformat('T')[:-7]+'+03:00',
          'title' : 'Журнал «Квантик»'
    }
    dir_path = 'local/gsheets2issue/'+i['year']+'/'
    directory = os.path.dirname(dir_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(dir_path+str(i['month'])+'.md', 'w', encoding = "utf-8") as output:
        #output.write('+++\n')
        #output.writelines(toml.dumps(i))
        #output.write('+++\n')
        output.write('---\n')
        output.writelines(yaml.dump(i, allow_unicode=True, width=120))
        output.write('---\n')
    
def slogan_quotes(slogan):
    slogan = list(slogan)
    quotes = [i for i,c in enumerate(slogan) if c=='"']
    for num, i in enumerate(quotes):
        if num%2==0:
            slogan[i] = "«"
        else:
            slogan[i] = "»"
    return ''.join(slogan)
    
#print(slogan_quotes('Избранные задачи конкурса "Кенгуру".'))

def get_pages(articles):
    def article_pages(a):
        first = int(a['first_page']) +2
        return range(first, first + int(a['npages']))

    pages = [article_pages(a) for a in articles if (a['in_sample']==True)]
    pages = [page for p in pages for page in p] + [2,3]
    return sorted(pages)
    
            
def make_sheet(gc, year, month):
    month = str(month).zfill(2) # 2 -> '02'
    year = str(year)
    def names_from_cell(string):
        def strip(item):
            if ':' in item:
                item = item.split(':')[1]
            return item.strip('{:} ')
        return [ strip(s) for s in string.split(';')]
        
    sheets = gc.open('Таблица выпусков для обновления сайта '+year)    
    sheet = sheets.worksheet(property='title', value=month)
    end = sheet.find('Фразы, не привязанные к статье')[0].row
    articles_table = sheet.get_values(start = (3,1), end = (end-1, 8), include_all = True)
    slogans = [ slogan_quotes(s) for s in sheet.get_col(7)[end:] ]
    all_slogans = [ slogan_quotes(s) for s in sheet.get_col(7)[1:] ]
    all_slogans = [s for s in all_slogans if s!='']
    articles = [{
            'year' : year,    
            'month' : month,    
            'first_page' : a[0],    
            'npages' : a[1],    
            'title' : a[2],
            'rubric'  : [a[3],],
            'authors' : names_from_cell(a[4]),
            'illustrators' : names_from_cell(a[5]),
            'slogan' : slogan_quotes(a[6]),
            'in_sample' : True if a[7].lower() == "да" else False,
    } for a in articles_table]
    for i, a in enumerate(articles):
        if a['first_page']=='34':
            a['npages']='1'
        elif a['first_page']=='-1':
            a['npages']='1'
        elif a['npages']=='':
            a['npages']=str(int(articles[i+1]['first_page'])-int(a['first_page']))
    #for a in articles:
    #    article2md(a)
    issue2md(year, month, all_slogans)
    if (year=='2017')  or (year == '2016' and int(month)>9):
        pages = get_pages(articles)
    else:
        pages = range(1,37)
    print(pages)
    pdf2jpg('local/pdfs/{0}-{1}.pdf'.format(year,month), pages)

gc = pygsheets.authorize(service_file='local/kvantik-gspread.json')
for year in range(2017, 2018):
    for month in range(6, 10):
        make_sheet(gc, str(year), str(month).zfill(2))
        print(year, month)
print('All done')
