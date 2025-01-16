from pydantic import BaseModel

class BasicStock(BaseModel):
    nombre: str
    simbolo: str
    ultimo_precio: str
    monto_efectivo: str
    variacion: str
    titulos_negociados: str

class StockDetail(BaseModel):
    desc_simbolo: str
    cod_simbolo: str
    cod_isin: str
    acciones_circulacion: str
    capitalizacion_en_mill: str
    moneda: str
    estado: str
    ultimo_precio: str
    cierre_anterior: str
    operaciones_del_dia: str
    titulos_del_dia: str
    efectivo_del_dia: str
    operaciones_anual: str
    titulos_anual: str
    efectivo_anual: str

class RentaVariable(BaseModel):
    operaciones: str
    titulos_negociados: str
    monto_en_efectivo_bs: str
    hora: str