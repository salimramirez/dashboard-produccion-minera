import httpx

from app.config import GOLDAPI_URL, GOLDAPI_TOKEN, TIMEOUT_SEGUNDOS
from app.datos import DATOS
from app.modelos import Precios

_cache: Precios | None = None


def _precios_de_respaldo() -> Precios:
    respaldo = DATOS.precios_fallback_usd_oz
    return Precios(oro=respaldo.oro, plata=respaldo.plata, origen="respaldo")


async def obtener_precios() -> Precios:
    global _cache
    if _cache is not None:
        return _cache

    if not GOLDAPI_TOKEN:
        return _precios_de_respaldo()

    try:
        cabeceras = {"x-access-token": GOLDAPI_TOKEN}
        async with httpx.AsyncClient(timeout=TIMEOUT_SEGUNDOS) as cliente:
            oro = await cliente.get(f"{GOLDAPI_URL}/XAU/USD", headers=cabeceras)
            plata = await cliente.get(f"{GOLDAPI_URL}/XAG/USD", headers=cabeceras)
            oro.raise_for_status()
            plata.raise_for_status()
            _cache = Precios(
                oro=oro.json()["price"], plata=plata.json()["price"], origen="api"
            )
            return _cache
    except Exception:
        return _precios_de_respaldo()
