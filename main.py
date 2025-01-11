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