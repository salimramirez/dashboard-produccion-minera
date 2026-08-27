from fastapi import HTTPException

from app.datos import DATOS
from app.modelos import DetalleMetal, Mina, Precios, ProduccionMensual, Valorizacion


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


def calcular_valorizacion(minas: list[Mina], precios: Precios) -> Valorizacion:
    total_oro = sum(registro.oro_oz for mina in minas for registro in mina.produccion)
    total_plata = sum(
        registro.plata_oz for mina in minas for registro in mina.produccion
    )

    valor_oro = round(total_oro * precios.oro, 2)
    valor_plata = round(total_plata * precios.plata, 2)

    return Valorizacion(
        total_usd=round(valor_oro + valor_plata, 2),
        oro=DetalleMetal(
            onzas=total_oro,
            precio_usd_oz=precios.oro,
            valor_usd=valor_oro,
        ),
        plata=DetalleMetal(
            onzas=total_plata,
            precio_usd_oz=precios.plata,
            valor_usd=valor_plata,
        ),
        origen_precios=precios.origen,
    )
