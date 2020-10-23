import common

def get_articles(tag):
    tables = {year:common.get_table(year) for year in range(2012, common.year+1)}
    articles = [{**i, **{'год':y}} for y, t in tables.items() for i in t]
    return [a for a in articles if tag in a['теги']]

def make_pdf(articles, filename, output_folder = None):
    if output_folder == None:
         output_folder = f'local/{filename}/'
    common.clear_folder(output_folder)
    issues_folder = common.pdfs()

    pages_copied = 0
    for t in articles:
        common.copy_article(issues_folder, t['год'], 
                    t['выпуск'], t['первая'], t['всего'], 
                    output_folder, str(pages_copied).zfill(3))
        pages_copied += int(t['всего'])
    common.bash(f'pdftk {output_folder}* cat output {output_folder}{filename}.pdf')
    return pages_copied

if __name__ == "__main__":
    tag = input('Введите тег для сбора в pdf: ')
    articles = get_articles(tag)
    common.to_csv(f'local/biblio-{tag}.csv', articles)
    make_pdf(articles, f'biblio-{tag}')