from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.rutas_compras import router as router_compras

app = FastAPI(title="EcoHarmony Park API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["POST"],
    allow_headers=["Content-Type", "X-Usuario-Email"],
)
app.include_router(router_compras)


@app.get("/salud")
def salud():
    return {"estado": "ok"}
