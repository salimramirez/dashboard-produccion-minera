from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import minas

app = FastAPI(
    title="Dashboard de Producción Minera",
    description="API de producción mensual de oro y plata y su valorización a precios de mercado",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def raiz():
    return {"mensaje": "API en funcionamiento"}


app.include_router(minas.router)
