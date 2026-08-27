from fastapi import APIRouter

from app.datos import DATOS
from app.modelos import Mina, ProduccionMensual, RegistroProduccion
from app.servicios.calculos import calcular_resumen, obtener_minas


router = APIRouter(prefix="/api", tags=["minas"])


@router.get("/minas", response_model=list[Mina])
def listar_minas():
    return DATOS.minas


@router.get("/produccion", response_model=list[RegistroProduccion])
def listar_produccion(mina_id: int | None = None, mes: str | None = None):
    minas = obtener_minas(mina_id)
    return [
        RegistroProduccion(
            mina_id=mina.id,
            nombre=mina.nombre,
            mes=registro.mes,
            oro_oz=registro.oro_oz,
            plata_oz=registro.plata_oz,
        )
        for mina in minas
        for registro in mina.produccion
        if mes is None or registro.mes == mes
    ]


@router.get("/resumen", response_model=list[ProduccionMensual])
def listar_resumen(mina_id: int | None = None):
    minas = obtener_minas(mina_id)
    return calcular_resumen(minas)
