#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cover
import pdf2konkurs




if __name__ == "__main__":

# подготовка черновиков для проверки и использования:
    print('Данный скрипт возьмёт pdf вида local/pdfs/2018-XX.pdf и выведет обложку и конкурс в папку local/2018-XX')
    print('Номер выпуска?')
    num=int(input())
    #print('local/pdfs/2018-{:0>2}.pdf'.format(num))
    pdf2konkurs.extract('local/pdfs/2018-{:0>2}.pdf'.format(num))
    cover.get_cover('local/pdfs/2018-{:0>2}.pdf'.format(num))    


# make sample: pdftk 2018-06.pdf cat 1-3 10-15 34-end output 2018-06_sample.pdf

# fetch issue info from spreadsheet and generate .md

# предложить проверить сгенерированные файлы

# предложить git pull и проверить ветку

# скопировать файлы куда надо

# git add, commit, push
