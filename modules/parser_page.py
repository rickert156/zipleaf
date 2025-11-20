import csv
import requests
import os
import sys
import shutil
from bs4 import BeautifulSoup
from SinCity.colors import RED, RESET, GREEN
from modules.config import (
        status_type_info, 
        status_type_warning, 
        status_type_error,
        company_url_file,
        )
from SinCity.Agent.header import header
from modules.miniTools import log_time

def divide():
    len_line = int(shutil.get_terminal_size().columns)
    divide_line = '-'*(len_line-2)
    return divide_line

def get_company_name(bs:str) -> str | None:
    company = None
    company = bs.find('span', {'itemprop':'name'})
    if company:company = company.get_text()
    return company

def get_phone(bs:str) -> str | None:
    phone = None
    block = bs.find(class_='txt-margin')
    if block:
        for line in block.find_all('p'):
            if 'Phone:' in line.get_text():
                phone = line.get_text().split('Phone: ')[1]
    return phone

def get_site(bs:str) -> str | None:
    site = None
    site = bs.find(class_='g_link')
    if site:site = site.get_text()
    return site

def get_location(bs:str) -> str | None:
    location = None
    location = bs.find('span', {'itemprop':'address'})
    if location:location = location.get_text()
    return location

def get_company_info(url:str) -> dict[str]:
    data = {'company':None, 'site':None, 'phone':None, 'location':None}
    divide_line = divide()
    head = header()
    response = requests.get(url, headers=head)
    status_code = response.status_code
    if status_code == 200:
        #print(f'{log_time()} {status_type_info} {GREEN}{url} OK{RESET}')
        bs = BeautifulSoup(response.text, 'lxml')
        content_block = bs.find(class_='box-content listing-container')
        company = get_company_name(bs=bs)
        phone = get_phone(bs=content_block)
        site = get_site(bs=content_block)
        location = get_location(bs=content_block)
        
        data['company'] = company
        data['site'] = site
        data['phone'] = phone
        data['location'] = location
        
    else:
        print(f'{log_time()} {status_type_warning} {RED}{url} {status_code}{RESET}')

    return data
        

if __name__ == '__main__':
    params = sys.argv
    if len(params) > 1 and '--page=' in params[1] \
            and 'https://www.zipleaf.us/Companies/' in params[1]:
            url = params[1].split('--page=')[1]
            data = get_company_info(url=url)
            print(data)
    else:
        print(
                f'Пример использования:\n'
                f'python3 -m modules.parser_page '
                f'--page="https://www.zipleaf.us/Companies/PKF-Hawaii"'
                )
