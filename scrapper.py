from selenium import webdriver
from selenium.webdriver.common.by import By
from const import url
import json


driver = webdriver.Chrome()
driver.get(url)
table = driver.find_element(By.ID, 'tbl-resumen-mercado')
print(table.text)