import common


def make_pdf(tag, output_folder = None):
    if output_folder == None:
         output_folder = f'local/biblio-{tag}/'
    common.clear_folder(output_folder)
    issues_folder = common.pdfs()
    

    tables = {year:common.get_table(year) for year in range(2012, 2020)}
    pages_copied = 0
    for year, table in tables.items():
        for t in table:
            if tag in t['теги']:
                common.copy_article(issues_folder, year, 
                    t['выпуск'], t['первая'], t['всего'], 
                    output_folder, str(pages_copied).zfill(3))
                pages_copied += int(t['всего'])
    common.bash(f'pdftk {output_folder}* cat output {output_folder}biblio-{tag}.pdf')


if __name__ == "__main__":
    make_pdf(input('Введите тег для сбора в pdf: '))