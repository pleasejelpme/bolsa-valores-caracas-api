from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models import BasicStock, StockDetail, RentaVariable
import json


app = FastAPI(
    title='Bolsa de Valores de Caracas API',
    description='API que propociona informacion de acciones cotizadas en la Bolsa de Valores de Caracas',
    version='1.0.0',
)


@app.get('/acciones', response_class=JSONResponse)
async def get_acciones_list() -> list[BasicStock]:
    """
    Retorna una lista de acciones cotizadas en la Bolsa de Valores de Caracas,
    obtenida de la pagina web de la Bolsa de Valores de Caracas.
    """
    file = open('json/stocks.json')
    return json.load(file)


@app.get('/renta-variable', response_class=JSONResponse)
async def get_renta_variable() -> RentaVariable:
    """
    Retorna informacion de la tabla "renta variable"
    obtenida de la pagina web de la Bolsa de Valores de Caracas.
    """
    file = open('json/renta_variable.json')
    return json.load(file)


@app.get('/acciones/{cod_simbolo}', response_class=JSONResponse)
async def get_accion_detalle(cod_simbolo: str) -> StockDetail:
    """
    Dado el codigo de la accion a consultar, retorna informacion detallada de la accion.

    ### Lista de codigos:
    * Bco. del Caribe Clase "A": **ABCA**
    * Arca Inm. y Valores Clase "B": **ARCB**
    * Bco. Provincial: **BPV**
    * Bolsa de Valores de Ccs: **BVCC**
    * Bco. de Venezuela: **BVL**
    * Corp. Grupo Quimico: **CGQ**
    * Corimon C.A.: **CRMA**
    * Dominguez y Cia.: **DOM**
    * Productos EFE: **EFE**
    * Envases Venezolanos: **ENV**
    * Grupo Mantra Corp: **GMCB**
    * Inversiones Crecepymes: **ICPB**
    * Invaca Clase "A": **IVCA**
    * Invaca Clase "B": **IVCB**
    * Manufacuras de Papel C.A.: **MPA**
    * Montesco: **MTCB**
    * Mercantil Servicios Financieros: **MVZB**
    * Proagro: **PGR**
    * Pivca: **PIVB**
    * Protinal: **PTN**
    * Ron Santa Teresa: **RST**
    * Ron Santa Teresa Clase "B": **RSTB**
    * Sivensa: **SVS**
    * Cantv: **TDVD**
    * Telares de Palo Grande: **TPG**
    * Venealterna: **VNAB**
    """

    cod_simbolo = cod_simbolo.upper()
    file = open('json/stocks_details.json')
    data = json.load(file)
    for stock in data:
        if stock['cod_simbolo'] == cod_simbolo:
            return stock
    
    return {'message': 'Stock not found'}