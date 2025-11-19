import csv
import os
import requests
from bs4 import BeautifulSoup
from modules.config import data_dir, source_categories_file, categories_file
from modules.miniTools import log_time
from SinCity.Agent.header import header

total_count = 0

def recording_count(id_:int, category:str, url:str, count:int) -> None:
    if not os.path.exists(categories_file):
        with open(categories_file, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Category', 'Count', 'URL'])

    with open(categories_file, 'a') as file:
        writer = csv.writer(file)
        writer.writerow([id_, category, count, url])

def get_count(url:str) -> str | int:
    global total_count
    head = header()
    response = requests.get(url, headers=head)
    if response.status_code == 200:
        bs = BeautifulSoup(response.text, 'lxml')
        count = bs.find('h4')
        if count != None and ' more results' in count.get_text():
            count = int(count.get_text().split(' more results')[0].replace(',', ''))
            total_count+=count
        return count
    else:
        return f'status code: {response.status_code}'

if __name__ == '__main__':
    with open(source_categories_file, 'r') as file:
        number_category = 0
        for row in csv.DictReader(file):
            number_category+=1
            category = row.get('Category')
            url = row.get('URL')

            count = get_count(url=url)
            print(f'{log_time()} [{number_category}] {category}\t\t{count}')
            recording_count(id_=number_category, category=category, count=count, url=url)

    with open(categories_file, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(['Total', '', '', total_count])
    print(f'Всего компаний в сервисе: {total_count}')
