from fastapi import HTTPException

from app.datos import DATOS
from app.modelos import Mina, ProduccionMensual


def obtener_minas(mina_id: int | None) -> list[Mina]:
    if mina_id is not None:
        mina_encontrada = next((m for m in DATOS.minas if m.id == mina_id), None)
        if mina_encontrada is None:
            raise HTTPException(status_code=404, detail="Mina no encontrada")
        minas = [mina_encontrada]
    else:
        minas = DATOS.minas
    return minas


def calcular_resumen(minas: list[Mina]) -> list[ProduccionMensual]:
    acumulado = {}
    for mina in minas:
        for registro in mina.produccion:
            if registro.mes not in acumulado:
                acumulado[registro.mes] = {"oro": 0, "plata": 0}
            acumulado[registro.mes]["oro"] += registro.oro_oz
            acumulado[registro.mes]["plata"] += registro.plata_oz
    return [
        ProduccionMensual(mes=mes, oro_oz=totales["oro"], plata_oz=totales["plata"])
        for mes, totales in sorted(acumulado.items())
    ]
