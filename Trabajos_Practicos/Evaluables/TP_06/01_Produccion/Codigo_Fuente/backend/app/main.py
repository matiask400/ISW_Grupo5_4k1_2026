from fastapi import FastAPI

from app.api.rutas_compras import router as router_compras

app = FastAPI(title="EcoHarmony Park API")
app.include_router(router_compras)


@app.get("/salud")
def salud():
    return {"estado": "ok"}
