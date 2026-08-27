from fastapi import APIRouter, HTTPException

from app.datos import DATOS
from app.modelos import Mina, RegistroProduccion


router = APIRouter(prefix="/api", tags=["minas"])


@router.get("/minas", response_model=list[Mina])
def listar_minas():
    return DATOS.minas

@router.get("/produccion", response_model=list[RegistroProduccion])
def listar_produccion(mina_id: int | None = None, mes: str | None = None):
    if mina_id is not None:
        mina_encontrada = next((m for m in DATOS.minas if m.id == mina_id), None)
        if mina_encontrada is None:
            raise HTTPException(status_code=404, detail="Mina no encontrada")
        minas = [mina_encontrada]
    else:
        minas = DATOS.minas

    return [
        RegistroProduccion(
            mina_id=mina.id,
            nombre=mina.nombre,
            mes=registro.mes,
            oro_oz=registro.oro_oz,
            plata_oz=registro.plata_oz
        )
        for mina in minas
        for registro in mina.produccion
        if mes is None or registro.mes == mes
    ]
