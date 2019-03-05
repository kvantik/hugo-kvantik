#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
import cover
import pdf2konkurs
import sample


if __name__ == "__main__":

# подготовка черновиков для проверки и использования:
    print('Данный скрипт возьмёт pdf вида local/pdfs/{0}-XX.pdf и выведет обложку, конкурс и сэмпл номера в папку local/{0}-XX'.format(common.year))
    print('Номер выпуска?')
    num = int(input())
    pdf = common.pdf(num)
    #print('local/pdfs/2018-{:0>2}.pdf'.format(num))
    pdf2konkurs.extract(pdf)
    cover.get_cover(pdf)    
    sample.make_sample(num, pdf)

# fetch issue info from spreadsheet and generate .md

# предложить проверить сгенерированные файлы

# предложить git pull и проверить ветку

# скопировать файлы куда надо

# git add, commit, push
