from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from models import BasicStock, StockDetail, RentaVariable
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime
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
        buffer = BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=letter)

        data = [['Nombre', 'Simbolo', 'Ultimo Precio (BS)', 'Monto Efectivo (BS)', 'Variacion', 'Titulos Negociados']]

        style = TableStyle([
            ('BACKGROUND', (0,0), (6,0), colors.lightgrey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMMARGIN', (0,0), (-1,0), 6),
            ('TOPPADDING', (0,0), (-1,0), 5),
            ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ])

        for item in acciones:
            data.append([item['nombre'], item['simbolo'], item['ultimo_precio'], item['monto_efectivo'], item['variacion'], item['titulos_negociados']])
        
        tabla = Table(data)
        tabla.setStyle(style)

        styles = getSampleStyleSheet()
        style_header = styles['Heading1']
        titulo = Paragraph(f'Acciones Cotizadas en la Bolsa de Valores de Caracas  |  {datetime.now().strftime("%d/%m/%Y")}', style_header)
        spacer = Spacer(1, 20)
        elements = []
        elements.append(titulo)
        elements.append(spacer)
        elements.append(tabla)
        pdf.build(elements)
        buffer.seek(0)
        acciones_pdf = buffer.getvalue()

        return Response(content=acciones_pdf, media_type='application/pdf', headers={'Content-Disposition': 'attachment; filename="acciones.pdf"'})