import csv
import requests
import os
import sys
from bs4 import BeautifulSoup
from SinCity.colors import RED, RESET, GREEN
from modules.config import (
        status_type_info, 
        status_type_warning, 
        status_type_error,
        company_url_file,
        complite_categories_url
        )
from SinCity.Agent.header import header
from modules.miniTools import log_time

def recording_company_url(url:str, company:str, location:str, category:str) -> None:
    if not os.path.exists(company_url_file):
        with open(company_url_file, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Company', 'URL', 'Location', 'Category'])

    with open(company_url_file, 'a') as file:
        writer = csv.writer(file)
        writer.writerow([company, url, location, category])

def get_complite_category_url() -> list[str]:
    list_url = set()
    if os.path.exists(complite_categories_url):
        with open(complite_categories_url, 'r') as file:
            for line in file.readlines():
                list_url.add(line.strip())
    return list_url

def recording_complite_url(url):
    with open(complite_categories_url, 'a') as file:
        file.write(f'{url}\n')

def get_max_page(bs:str) -> int:
    """Получаем максимальное количество страниц поиска по категории"""
    max_page = None
    pagination = bs.find(id='pagination')
    if pagination:
        max_page = pagination.find(class_='title').get_text().split('of ')[1].split(' |')[0]
    if max_page:max_page = int(max_page.strip())
    return max_page

def start_get_companies(url:str) -> None:
    if url in get_complite_category_url():
        return
    try:
        head = header()
        response = requests.get(url, headers=head)
        status_code = response.status_code
        if status_code == 200:
            print(f'{log_time()} {status_type_info} {url}: {GREEN}OK{RESET}')
            bs = BeautifulSoup(response.text, 'lxml')
            max_page = get_max_page(bs=bs)
            get_companies(url=url, max_page=max_page)
        else:
            print(f'{log_time()} {status_type_warning} {url}: {RED}{status_code}{RESET}')
    except KeyboardInterrupt:
        sys.exit(f'\n{RED}Exit...{RESET}')

def get_companies(url:str, max_page:int):
    category = url.split('https://www.zipleaf.us/Products/')[1]
    try:
        if max_page:
            page = 1
            complite_url_list = get_complite_category_url()
            for page in range(max_page+1):
                page+=1
                full_url = f'{url}/{page}'
                if full_url not in complite_url_list:
                    print(full_url)
                    head = header()
                    response = requests.get(full_url, headers=head)
                    status_code = response.status_code
                    if status_code == 200:
                        print(f'{log_time()} {status_type_info} {full_url}: {GREEN}OK{RESET}')
                        bs = BeautifulSoup(response.text, 'lxml')
                        list_block = bs.find_all(class_='listings')
                        number_block=0
                        for block in list_block:
                            company = block.find('h3')
                            location = block.find(class_='address')

                            if company:
                                link = f"https://www.zipleaf.us{company.find('a').get('href')}"
                                company = company.get_text()
                            if location:location = location.get_text()

                            if company:
                                number_block+=1
                                print(
                                        f'[{number_block}]'
                                        f'Company:\t{company}\n'
                                        f'Link:\t\t{link}\n'
                                        f'Location:\t{location}\n'
                                        f'Category:\t{category}\n'
                                        )
                                recording_company_url(
                                        url=link, 
                                        company=company, 
                                        location=location,
                                        category=category
                                        )
                                recording_complite_url(url=full_url)
                        

                    else:
                        print(
                                f'{log_time()} {status_type_warning} '
                                f'{url}: {RED}{status_code}{RESET}'
                                )
            recording_complite_url(url=url)
    except KeyboardInterrupt:
        sys.exit(f'\n{RED}Exit...{RESET}')

if __name__ == '__main__':
    params = sys.argv
    if len(params) > 1 and '--parser-page=' in params[1] and 'http' in params[1]:
        url = params[1].split('--parser-page=')[1].strip()
        start_get_companies(url=url)
    else:
        print(
                f'Пример использования:\n'
                f'python3 -m modules.parser_category '
                f'--parser-page="https://www.zipleaf.us/Products/County"'
                )

