#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
import cover
import konkurs
import sample


if __name__ == "__main__":

# подготовка черновиков для проверки и использования:
    print('Данный скрипт возьмёт pdf вида local/pdfs/{0}-XX.pdf и выведет обложку, конкурс и сэмпл номера в папку local/{0}-XX'.format(common.year))
    num = int(input('Номер выпуска? '))
    pdf = common.pdf(num)
    #print('local/pdfs/2018-{:0>2}.pdf'.format(num))
    konkurs.extract(pdf)
    cover.get_cover(pdf)    
    sample.make_sample(num, pdf)
    print('а также обновит csv-файлы в папке local')
    common.update_csv()

# fetch issue info from spreadsheet and generate .md

# предложить проверить сгенерированные файлы

# предложить git pull и проверить ветку

# скопировать файлы куда надо

# git add, commit, push
