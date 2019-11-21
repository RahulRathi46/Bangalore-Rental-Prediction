from json import loads, load

with open('../Data_Scraper/raw.json') as json_file:
    r = load(json_file)

for i in r:
    print(i['desc'])