from app.datos import DATOS
from app.modelos import Precios


def obtener_precios() -> Precios:
    respaldo = DATOS.precios_fallback_usd_oz
    return Precios(oro=respaldo.oro, plata=respaldo.plata, origen="respaldo")
