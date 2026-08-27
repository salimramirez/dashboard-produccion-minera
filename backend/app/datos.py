import json
from pathlib import Path

from app.modelos import DatosProduccion

RUTA_DATOS = Path(__file__).parent.parent / "datos_produccion.json"

DATOS = DatosProduccion.model_validate(
    json.loads(RUTA_DATOS.read_text(encoding="utf-8"))
)
