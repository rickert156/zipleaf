from bs4 import BeautifulSoup 
from SinCity.colors import RED, RESET, GREEN, BLUE, YELLOW
from SinCity.Browser.driver_chrome import driver_chrome
from SinCity.Agent.header import header
from typing import Optional
from modules.logger import log_print
from modules.miniTools import (
        init_parser, 
        log_time, 
        parse_params
        )
from modules.config import (
        status_type_error, 
        status_type_warning,
        status_type_info
        )
import requests
import sys
import time

def parser_result(url:str, parser:Optional[str]=None) -> None:
    mode = parser if parser else 'selenium'
    
    log_print(f'{log_time()} {status_type_info} Тип парсера:\t{mode}')
    
    if mode == 'requests':
        head = header()
        response = requests.get(url, headers=head)
        status_code = response.status_code
        if status_code == 200:
            log_print(f'{log_time()} {status_type_info} Доступ к URL: {GREEN}OK{RESET}')
        else:
            log_print(f'{log_time()} {status_type_error} Status code: {RED}{status_code}{RESET}')
    else:
        driver = None
        try:
            driver = driver_chrome()
            driver.get(url)
            page_source = driver.page_source
            bs = BeautifulSoup(page_source, 'lxml')
            if 'Cloudflare' in bs.body.get_text():
                log_print(f'{log_time()} {status_type_warning} Проверка Cloudflare')
                driver.quit()
                parser_result(url=url)
            else:
                log_print(f'{log_time()} {status_type_info} Проверка Cloudflare не обнаружена')
        except Exception as err:
            log_print(f'{log_time()} {status_type_error} Error: {err}')
        finally:
            if driver:
                driver.quit()

if __name__ == '__main__':
    try:
        #инит парсера - создаем директории и подобное
        init_parser()
        #убрать имя скрипта
        params = sys.argv[1:]
    
        args = parse_params(params=params)
    
        if len(args) != 0:
            #print(args)
            test_url = args['--test-url'] if args.get('--test-url') else None 
            parser = args['--parser'] if args.get('--parser') else None 
            
            parser_mode_list = ['requests', 'selenium', None]

            if parser not in parser_mode_list:
                sys.exit(
                        f'{log_time()} {status_type_error} '
                        f'Выбери из доступных методов: {parser_mode_list[0:-1]}')
    
            if test_url:
                parser_result(url=test_url, parser=parser)
        if len(args) == 0:
            log_print(f'{log_time()} {status_type_warning} необходимо передать параметры')
    except KeyboardInterrupt:
        sys.exit(f'\n{log_time()} {status_type_info} Exit...')
    except Exception as err:
        log_print(f'{log_time()} {status_type_warning} {err}')
