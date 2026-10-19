import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.rutas_compras import router as router_compras

FRONTEND_LOCAL = "http://localhost:5173"


def origenes_permitidos(configurados: str | None) -> list[str]:
    """El frontend local más los de ORIGENES_PERMITIDOS (separados por coma)."""
    extras = [origen.strip().rstrip("/") for origen in (configurados or "").split(",")]
    return [FRONTEND_LOCAL, *(origen for origen in extras if origen)]


app = FastAPI(title="EcoHarmony Park API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes_permitidos(os.getenv("ORIGENES_PERMITIDOS")),
    allow_methods=["POST"],
    allow_headers=["Content-Type", "X-Usuario-Email"],
)
app.include_router(router_compras)


@app.get("/salud")
def salud():
    return {"estado": "ok"}
