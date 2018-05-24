#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cover
import pdf2konkurs



if __name__ == "__main__":
    print('Данный скрипт возьмёт pdf вида local/pdfs/2018-XX.pdf и выведет обложку и конкурс в папку local/2018-XX')
    print('Номер выпуска?')
    num=int(input())
    #print('local/pdfs/2018-{:0>2}.pdf'.format(num))
    pdf2konkurs.extract('local/pdfs/2018-{:0>2}.pdf'.format(num))
    cover.get_cover('local/pdfs/2018-{:0>2}.pdf'.format(num))    

# take issue and complete/preview/both from arguments

# gspread fetch issue info

# git pull

# generate issue and articles .md pages

# take pdf from somewhere (argument for starters) and generate pages' images to static

# remove temporary files

# git add, commit, push