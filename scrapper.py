from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from const import url
from utils import remove_dots
import json
import os


def setup_driver() -> webdriver.Chrome:
    """
    Set up a selenium web driver and returns it ready for scrapping the web page.
    """

    try: 
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        return driver
    except Exception as e:
        print(f'Error: {e}')
        return None


def scrapp_page(driver: webdriver.Chrome) -> BeautifulSoup:
    """
    Takes an WebDriver object and returns a BeautifulSoup object of the web page, ready for scrapping.
    """
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def scrapp_single_items(driver: webdriver.Chrome) -> list:
    """
    Given a selenium web driver, finds the "resumen mercado" table, clicks on every item in the table
    and get the detailed data of every stock. Returns a list with the data cleaned.
    """

    data = []
    rows = driver.find_elements(By.CSS_SELECTOR, '[data-load="detalle"]')

    for row in rows:
        try:
            wait = WebDriverWait(driver, 10)
            actions = ActionChains(driver)
            actions.move_to_element(row).perform()
            driver.execute_script('arguments[0].click();', row)
            table = wait.until(EC.visibility_of_element_located((By.ID, 'detalle-simbolo')))
            stock = {
                'desc_simbolo': table.find_element(By.ID, 'desc-simbolo').text,
                'cod_simbolo': remove_dots(table.find_element(By.ID, 'cod-simbolo').text),
                'cod_isin': table.find_element(By.ID, 'cod-isin').text,
                'acciones_circulacion': table.find_element(By.ID, 'acciones-circulacion').text,
                'capitalizacion_en_mill': table.find_element(By.ID, 'capitalizacion').text,
                'moneda': table.find_element(By.ID, 'moneda').text,
                'estado': table.find_element(By.ID, 'estado').text,
                'ultimo_precio': table.find_element(By.ID, 'precio').text,
                'cierre_anterior': table.find_element(By.ID, 'cierre_ant').text,
                'operaciones_del_dia': table.find_element(By.ID, 'operaciones').text,
                'titulos_del_dia': table.find_element(By.ID, 'titulos').text,
                'efectivo_del_dia': table.find_element(By.ID, 'efectivo').text,
                'operaciones_anual': table.find_element(By.ID, 'operacionesAnual').text,
                'titulos_anual': table.find_element(By.ID, 'titulosAnual').text,
                'efectivo_anual': table.find_element(By.ID, 'efectivoAnual').text,
            }
            data.append(stock)
        
        except:
            print('Error: Could not get the data of the stocks')
    
    return data


def get_stocks(soup: BeautifulSoup) -> list:
    """
    Given a BeautifulSoup object, finds the "resumen mercado" table, scrapps the data of
    every item in the table, and return a list with the data cleaned.
    """

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


def get_renta_variable(soup: BeautifulSoup) -> list:
    """
    Finds the "rentavariable" table in the web page, scrapps the data of the table and returns a list
    with the data cleaned.
    """

    data = []
    cleaned_data = []
    keys = ['operaciones', 'titulos_negociados', 'monto_en_efectivo_bs', 'hora']

    table_renta_variable = soup.find(id='tbody-rentavariable')
    renta_variable = table_renta_variable.find_all('td')

    for item in renta_variable:
        data.append(item.string)

    data = [x for x in data if x is not None]
    renta = dict(zip(keys, data))
    cleaned_data.append(renta)

    return cleaned_data


def dump_json(filename: str, data: list) -> None:
    """
    Given a list, dumps the data into a json file.
    """

    with open(f'{filename}.json', 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    driver = setup_driver()
    soup = scrapp_page(driver)
    stocks = get_stocks(soup)
    renta_variable = get_renta_variable(soup)
    stock_details = scrapp_single_items(driver)

    if 'json' not in os.listdir():
        os.mkdir('json')
    
    os.chdir('json')
    dump_json(filename='stocks', data=stocks)
    dump_json(filename='renta_variable', data=renta_variable)
    dump_json(filename='stocks_details', data=stock_details)
    
    driver.quit()
