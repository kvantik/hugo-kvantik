from subprocess import call, check_output
import os
from functools import lru_cache

repo_root = '../'  

@lru_cache()
def pdfs():
    default = '../../small-pdfs/issues/'
    pdfs = input("Введите путь к папке с маленькими файлами журнала (Enter для {}):".format(default))
    if pdfs == '':
      pdfs = default
    if pdfs[-1]!= '/':
      pdfs = pdfs + '/'
    return pdfs
     
     
year = 2019


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
    