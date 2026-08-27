from pydantic import BaseModel


class ProduccionMensual(BaseModel):
    mes: str
    oro_oz: int
    plata_oz: int


class Mina(BaseModel):
    id: int
    nombre: str
    region: str
    produccion: list[ProduccionMensual]


class PreciosRespaldo(BaseModel):
    oro: float
    plata: float


class DatosProduccion(BaseModel):
    descripcion: str
    unidad: str
    anio: int
    minas: list[Mina]
    precios_fallback_usd_oz: PreciosRespaldo
