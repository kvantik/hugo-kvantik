def pdfs():
    default = '../../small-pdfs/issues/'
    pdfs = input("Введите путь к папке с маленькими файлами журнала (Enter для {}):".format(default))
    if pdfs == '':
      pdfs = default
    if pdfs[-1]!= '/':
      pdfs = pdfs + '/'
    return pdfs
     
     
year = 2019

def pdf(num):
  return '{0}{1}-{2:02}.pdf'.format(pdfs(), year, num)