import xml.etree.ElementTree as xml
from os import walk
import pandas as pd
import datetime
import csv
import dload


# ------ Парсинг
# Обращение к источникам данных
sources_zip = ['https://file.nalog.ru/opendata/7707329152-rsmp/data-10112022-structure-10032022.zip',
			'https://file.nalog.ru/opendata/7707329152-rsmppp/data-20221015-structure-20201220.zip']

sources_other = ['https://opendata.fssp.gov.ru/7709576929-iplegallist/data-20221112-structure-20220620.csv',
			'https://rosstat.gov.ru/storage/mediabank/tab4-zpl.xlsx',
			'https://rosstat.gov.ru/storage/mediabank/Oborot-09.xls']

for source in sources_other:
	dload.save(source)
print('Done others!')

for source in sources_zip:
	dload.save_unzip(source)

print('Done zip!')

filenames = next(walk('C:\\Users\\Гамид\\Desktop\\hack\\data-10102022-structure-10032022'), (None, None, []))[2]

filenames_gov_sup = next(walk('C:\\Users\\Гамид\\Desktop\\hack\\data-20221015-structure-20201220'), (None, None, []))[2]

# Формирование зависимостей код региона-регион
gov_sup_set = set()
bad_behav_set = set()
count = 0
region_num_dict = dict()
region_info_by_num_dict = dict()

excel_data = pd.read_excel('reg.xlsx', index_col=None, header=None)
for name in excel_data.iterrows():
	region_num_dict[name[1].tolist()[1].replace('\xa0', ' ')] = name[1].tolist()[0]

#print(region_num_dict)

excel_data = pd.read_excel('regions.xlsx', index_col=None, header=None)
for name in excel_data.iterrows():
	region_info_by_num_dict[region_num_dict[name[1].tolist()[0]]] = [name[1].tolist()[1], name[1].tolist()[2]]

#print(region_info_by_num_dict)

# Агрегирование данных по гос. поддержке
for file in filenames_gov_sup:
	tree = xml.ElementTree(file='data-20221015-structure-20201220\\' + file)
	root = tree.getroot()
	for i in range(1, len(root)):
		print(count)
		count += 1
		try:
			gov_sup_set.add(root[i][0].attrib['ИННФЛ'])
		except:
			pass

# Получение заголовков большого файла с судебными решениями, который не открывается и не позволяет корректно написать ключ, так как не открывается
'''
with open('data-20221110-structure-20220620.csv', 'r', encoding='utf-8') as f:
	d_reader = csv.DictReader(f)
	headers = d_reader.fieldnames
print(headers)
'''

# Агрегирование данных по задолженностям
bad_behav_df = pd.read_csv('data-20221110-structure-20220620.csv')
bad_behav_set = list(set(bad_behav_df['Debtor TIN'].tolist()))

#print(bad_behav_set[0], len(bad_behav_set), type(bad_behav_set[0]))

# Отлавливаем выбросы в исходных данных, которые приводят к ошибке программы
bugs_f = open('bugs_log.txt', 'a')

# Формирование основной таблицы согласно полям: ИНН, время жизни, регион, ОКВЭД, средняя ЗП по региону, оборот роз. торг. по региону, задолженность, гос. поддержка
df_cols = ['inn', 'lifetime', 'region', 'okved', 'average salary', 'oborot', 'bad_behav', 'gov_sup']
rows = []
count = 0
for file in filenames:
	tree = xml.ElementTree(file='data-10102022-structure-10032022\\' + file)
	root = tree.getroot()
	for i in range(1, len(root)):
		try:
			print(count)
			count += 1
			if root[i].attrib['ВидСубМСП'] == '2':
				rows.append({'inn': root[i][0].attrib['ИННФЛ'],
							'lifetime': (datetime.datetime.now() - datetime.datetime.strptime(root[i].attrib['ДатаВклМСП'], '%d.%m.%Y')).days,
							'region': root[i][1].attrib['КодРегион'],
							'okved': root[i][2][0].attrib['КодОКВЭД'],
							'average salary': region_info_by_num_dict[int(root[i][1].attrib['КодРегион'])][0],
							'oborot': region_info_by_num_dict[int(root[i][1].attrib['КодРегион'])][1],
							'bad_behav': 1 if float(root[i][0].attrib['ИННФЛ']) in bad_behav_set else 0,
							'gov_sup': 1 if root[i][0].attrib['ИННФЛ'] in gov_sup_set else 0})
		except Exception as e:
			bugs_f.write(str(e) + '\n')
bugs_f.close()
print(rows)

# Сохраняем сформированную таблицу
out_df = pd.DataFrame(rows, columns = df_cols)
out_df.to_csv('out.csv')
