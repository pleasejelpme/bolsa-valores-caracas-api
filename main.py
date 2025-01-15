from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json


app = FastAPI()

@app.get('/acciones', response_class=JSONResponse)
async def acciones():
    file = open('json/stocks.json')
    return json.load(file)

@app.get('/renta-variable', response_class=JSONResponse)
async def renta_variable():
    file = open('json/renta_variable.json')
    return json.load(file)

@app.get('/acciones/{cod_simbolo}', response_class=JSONResponse)
async def acciones_detail(cod_simbolo: str):
    cod_simbolo = cod_simbolo.upper()
    file = open('json/stocks_details.json')
    data = json.load(file)
    for stock in data:
        if stock['cod_simbolo'][0:3] == cod_simbolo:
            return stock
    
    return {'message': 'Stock not found'}