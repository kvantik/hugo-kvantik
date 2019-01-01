#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cover
import pdf2konkurs
import sample


if __name__ == "__main__":
    year = 2019

# подготовка черновиков для проверки и использования:
    print('Данный скрипт возьмёт pdf вида local/pdfs/{0}-XX.pdf и выведет обложку, конкурс и сэмпл номера в папку local/{0}-XX'.format(year))
    print('Номер выпуска?')
    num = int(input())
    pdf = 'local/pdfs/{0}-{1:0>2}.pdf'.format(year, num)
    #print('local/pdfs/2018-{:0>2}.pdf'.format(num))
    pdf2konkurs.extract(pdf)
    cover.get_cover(pdf)    
    sample.make_sample(num, pdf)

# fetch issue info from spreadsheet and generate .md

# предложить проверить сгенерированные файлы

# предложить git pull и проверить ветку

# скопировать файлы куда надо

# git add, commit, push
