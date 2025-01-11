from selenium import webdriver
from bs4 import BeautifulSoup
from const import url
import json
import os



def scrapp():
    """
    Using selenium and bs4, scrapps the BVC web page.

    Returns: A dictonary of arrays that contains data from market recap of BVC
    """
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_stocks(soup) -> list:
    data = []
    cleaned_data = []
    keys = ['nombre', 'simbolo', 'ultimo_precio', 'monto_efectivo', 'variacion', 'titulos_negociados']

    table_stocks = soup.find(id='tbl-resumen-mercado')
    rows = table_stocks.find_all('td')

    for row in rows:
        data.append(row.string)
    
    data = [x for x in data if x is not None]

    i = 0 
    while i < len(data):
        stock = dict(zip(keys, data[i:i+6]))
        cleaned_data.append(stock)
        i+=6        

    return cleaned_data


def get_renta_variable(soup) -> list:
    data = []
    cleaned_data = []
    keys = ['operaciones', 'titulos_negociados', 'monto_en_efectivo_bs', 'hora_24']

    table_renta_variable = soup.find(id='tbody-rentavariable')
    renta_variable = table_renta_variable.find_all('td')

    for item in renta_variable:
        data.append(item.string)

    data = [x for x in data if x is not None]
    renta = dict(zip(keys, data))
    cleaned_data.append(renta)

    return cleaned_data


def dump_json(filename, data):
    with open(f'{filename}.json', 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    soup = scrapp()
    stocks = get_stocks(soup)
    renta_variable = get_renta_variable(soup)

    if 'json' not in os.listdir():
        os.mkdir('json')
    
    os.chdir('json')
    dump_json(filename='stocks', data=stocks)
    dump_json(filename='renta_variable', data=renta_variable)

