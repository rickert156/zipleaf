import csv
import os
import sys
from SinCity.colors import RED, RESET, GREEN
from modules.parser_page import get_company_info, divide
from modules.config import company_url_file, complite_company_url, result_file_path

def recording_complite_company(url:str) -> None:
    with open(complite_company_url, 'a') as file:
        file.write(f'{url}\n')

def get_complite_company_url() -> list[str]:
    list_url = set()
    if os.path.exists(complite_company_url):
        with open(complite_company_url, 'r') as file:
            for line in file.readlines():
                list_url.add(line.strip())
    return list_url

def get_company_count() -> int:
    number_row=0
    with open(company_url_file, 'r') as file:
        for row in csv.DictReader(file):
            number_row+=1
    return number_row

def recording_company_info(
        company:str, 
        site:str, 
        location:str, 
        address:str, 
        phone:str, 
        category:str
        ):
    if not os.path.exists(result_file_path):
        with open(result_file_path, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Company', 'Site', 'Phone', 'Category', 'Location', 'Address'])

    with open(result_file_path, 'a') as file:
        writer = csv.writer(file)
        writer.writerow([company, site, phone, category, location, address])


def crowler_service():
    divide_line = divide()
    len_list_company = get_company_count()
    complite_company_url = get_complite_company_url()

    with open(company_url_file, 'r') as file:
        number_company = 0
        for row in csv.DictReader(file):
            number_company+=1
            url = row.get('URL')
            category = row.get('Category')
            location = row.get('Location')
            if url not in complite_company_url:
                company_info = get_company_info(url=url)
                company = company_info['company']
                site = company_info['site']
                phone = company_info['phone']
                address = company_info['location']
                print(
                        f'{GREEN}{divide_line}\n{RESET}'
                        f'[ {GREEN}{number_company} / {RED}{len_list_company}{RESET} ] '
                        f'{url} {category}'
                        f'Company:\t{company}\n'
                        f'Site:\t\t{site}\n'
                        f'Phone:\t\t{phone}\n'
                        f'Location:\t{location}'
                        )
                recording_company_info(
                        company=company,
                        site=site,
                        phone=phone,
                        location=location,
                        address=address,
                        category=category
                        )
                recording_complite_company(url=url)

if __name__ == '__main__':
    try:
        crowler_service()
    except KeyboardInterrupt:
        sys.exit(f'\n{RED}Exit...{RESET}')
