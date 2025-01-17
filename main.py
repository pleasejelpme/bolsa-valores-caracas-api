from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from models import BasicStock, StockDetail, RentaVariable
from pdf_builder import build_stocks_table
import json


app = FastAPI(
    title='Bolsa de Valores de Caracas API',
    description='API que propociona informacion de acciones cotizadas en la Bolsa de Valores de Caracas',
    version='1.0.0',
)


@app.get('/acciones', response_class=JSONResponse)
def get_acciones_list() -> list[BasicStock]:
    """
    Retorna una lista de acciones cotizadas en la Bolsa de Valores de Caracas,
    obtenida de la pagina web de la Bolsa de Valores de Caracas.
    """
    with open('json/stocks.json') as file:
        acciones = json.load(file)
        return [BasicStock(**accion) for accion in acciones]


@app.get('/renta-variable', response_class=JSONResponse)
def get_renta_variable() -> RentaVariable:
    """
    Retorna informacion de la tabla "renta variable"
    obtenida de la pagina web de la Bolsa de Valores de Caracas.
    """
    with open('json/renta_variable.json') as file:
        renta_variable = json.load(file)
        return RentaVariable(**renta_variable[0])


@app.get('/acciones/{cod_simbolo}', response_class=JSONResponse)
def get_accion_detalle(cod_simbolo: str) -> StockDetail:
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
    with open('json/stocks_details.json') as file:
        data = json.load(file)
        for stock in data:
            if stock['cod_simbolo'] == cod_simbolo:
                return StockDetail(**stock)

    return JSONResponse(
        status_code=404, 
        content={'message': 'Codigo de accion no encontrado. Verifica que es uno de los codigos listados en la documentacion.'}
        )


"""
Possible aditional features:
* Add a route that returns a PDF with the stocks information.
"""


@app.get('/pdf-acciones', response_class=Response)
def get_acciones_list_pdf() -> Response:
    with open('json/stocks.json', 'r', encoding='utf-8') as file:
        acciones = json.load(file)
        acciones_pdf = build_stocks_table(acciones)
        return Response(content=acciones_pdf, media_type='application/pdf', headers={'Content-Disposition': 'attachment; filename="acciones.pdf"'})