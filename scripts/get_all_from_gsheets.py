import common

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

sheets = [common.get_table(i,gsheet=True) for i in range(2012,2021)]

articles = [merge_two_dicts(a,{'Год':year}) for year in range(2012,2021) for a in sheets[year-2012]]


keys = set.union(*[set(a.keys()) for a in articles])

keys_dict = {key:'' for key in keys}

articles_full = [merge_two_dicts(keys_dict,a) for a in articles]

articles_sorted = []
for y in range(2020,2011,-1):
    for m in range(12,0,-1):
        articles_sorted += [a for a in articles_full if a['Год']==y and a['выпуск']==str(m)]

common.to_csv('all.csv',articles_sorted,delimiter='&')


allfields = lambda d: ''.join([str(k) for k in d.values()])
trash = [a for a in articles_full if a['выпуск'] not in [str(i) for i in range(13)]]
trash = [merge_two_dicts(t,{'Год':''}) for t in trash]
merged_trash = [allfields(t) for t in trash]
filtered_trash = [t for t in merged_trash if len(t)!=0]