from typing import Literal

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


class RegistroProduccion(BaseModel):
    mina_id: int
    nombre: str
    mes: str
    oro_oz: int
    plata_oz: int


class Precios(BaseModel):
    oro: float
    plata: float
    origen: Literal["api", "respaldo"]


class DetalleMetal(BaseModel):
    onzas: int
    precio_usd_oz: float
    valor_usd: float


class Valorizacion(BaseModel):
    total_usd: float
    oro: DetalleMetal
    plata: DetalleMetal
    origen_precios: Literal["api", "respaldo"]
