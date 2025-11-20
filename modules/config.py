from SinCity.colors import RED, RESET, GREEN, BLUE, YELLOW

#директории/файл для хранения инфы
result_dir = 'Result'
result_file = 'result.csv'
result_file_path = f'{result_dir}/{result_file}'
company_url_file = f'{result_dir}/company_url.csv'

data_dir = 'Data'
source_categories_file = f'{data_dir}/categories.csv'
categories_file = f'{data_dir}/company_count.csv'
complite_categories_url = f'{data_dir}/complite_categories_url.txt'
complite_company_url = f'{data_dir}/complite_company_url.txt'


#статусы
status_type_info = f"[{GREEN}INFO{RESET}]"
status_type_error = f"[{RED}ERROR{RESET}]"
status_type_warning = f"[{YELLOW}WARNING{RESET}]"
