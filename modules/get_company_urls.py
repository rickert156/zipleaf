import csv
from modules.config import categories_file 
from modules.parser_category import start_get_companies

if __name__ == '__main__':
    with open(categories_file, 'r') as file:
        number_category = 0
        for row in csv.DictReader(file):
            number_category+=1
            url = row.get('URL')
            print(f'[{number_category}] {url}')
            start_get_companies(url=url)
