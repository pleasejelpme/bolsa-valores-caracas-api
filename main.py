from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from models import BasicStock, StockDetail, RentaVariable
from scrapper import scrape_and_save
from pdf_builder import build_stocks_table
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from logger import logger
import json


scheduler = BackgroundScheduler()
trigger = CronTrigger(hour=10, minute=00, timezone='America/Caracas')
trigger2 = CronTrigger(hour=17, minute=19, timezone='America/Caracas')
scheduler.add_job(scrape_and_save, trigger)
scheduler.add_job(scrape_and_save, trigger2)
scheduler.start()

logger = logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Server up and running')
    yield
    logger.info('Server shutting down')
    scheduler.shutdown()

app = FastAPI(
    title='Bolsa de Valores de Caracas API',
    description='API que propociona informacion de acciones cotizadas en la Bolsa de Valores de Caracas',
    version='1.0.0',
    lifespan=lifespan
)


@app.get('/acciones', response_class=JSONResponse)
def get_acciones_list() -> list[BasicStock]:
    """
    Retorna una lista de acciones cotizadas en la Bolsa de Valores de Caracas,
    obtenida de la pagina web de la Bolsa de Valores de Caracas.
    """
    try:
        with open('json/stocks.json') as file:
            acciones = json.load(file)
            return [BasicStock(**accion) for accion in acciones]
    except:
        return Response(content='Error al obtener la informacion', status_code=500)


@app.get('/renta-variable', response_class=JSONResponse)
def get_renta_variable() -> RentaVariable:
    """
    Retorna informacion de la tabla "renta variable"
    obtenida de la pagina web de la Bolsa de Valores de Caracas.
    """
    
    try:
        with open('json/renta_variable.json') as file:
            renta_variable = json.load(file)
            return RentaVariable(**renta_variable[0])
    except:
        return Response(content='Error al obtener la informacion', status_code=500)
    

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
    
    try:
        with open('json/stocks_details.json') as file:
            data = json.load(file)
            for stock in data:
                if stock['cod_simbolo'] == cod_simbolo:
                    return StockDetail(**stock)

        return JSONResponse(
            status_code=404, 
            content={'message': 'Codigo de accion no encontrado. Verifica que es uno de los codigos listados en la documentacion.'}
            )
    except:
        Response(content='Error al obtener la informacion', status_code=500)


"""
Possible aditional features:
* Add a route that returns a PDF with the stocks information.
"""


@app.get('/pdf-acciones', response_class=Response)
def get_acciones_list_pdf() -> Response:
    """
    Entrega la informacion conseguida en el endpoint **/acciones** en formato PDF.
    """

    try: 
        with open('json/stocks.json', 'r', encoding='utf-8') as file:
            acciones = json.load(file)
            acciones_pdf = build_stocks_table(acciones)
            return Response(
                content=acciones_pdf, 
                media_type='application/pdf', 
                headers={'Content-Disposition': f'attachment; filename="acciones bvc {datetime.now().strftime("%d-%m-%y")}.pdf"'})
    except:
        return Response(content='Error al generar el PDF', status_code=500)