#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cover
import pdf2konkurs
import sample



if __name__ == "__main__":

# подготовка черновиков для проверки и использования:
    print('Данный скрипт возьмёт pdf вида local/pdfs/2018-XX.pdf и выведет обложку, конкурс и сэмпл номера в папку local/2018-XX')
    print('Номер выпуска?')
    num = int(input())
    pdf = 'local/pdfs/2018-{:0>2}.pdf'.format(num)
    #print('local/pdfs/2018-{:0>2}.pdf'.format(num))
    pdf2konkurs.extract(pdf)
    cover.get_cover(pdf)    
    sample.make_sample(num, pdf)

# fetch issue info from spreadsheet and generate .md

# предложить проверить сгенерированные файлы

# предложить git pull и проверить ветку

# скопировать файлы куда надо

# git add, commit, push
