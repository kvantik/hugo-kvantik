import common
import fileinput
import shutil

def issue2full(year, num):
    input('Убедитесь командой git pull, что в репозитории последняя версия. Нажмите "ввод" для продолжения или Ctrl+C для отмены.')
    md_file = common.repo_root + 'content/issue/{0}/{1:02}.md'.format(year, num) 
    with fileinput.FileInput(md_file, inplace=1) as file:
        for line in file:
            #print(line)
            if 'sample' in line:
                line = line.replace('true', 'false')
            print(line, end='')
    shutil.copy2(common.pdf(num, year = year), common.repo_root + 'static/issue/pdf/')

def  move_everything(num):
    pass
    
if __name__ == "__main__":
    while input('Хотите ли сделать заменить сэмплы на полные версии (да/нет, ввод = да)? ') in ['да', '']:
            year = input('Введите год выпуска (ввод для текущего): ')
            year = common.year if year == '' else int(year)
            issue2full(year , int(input('Введите месяц выпуска: ')) )
    num=int(input('Номер выпуска: '))
    move_everything(num)