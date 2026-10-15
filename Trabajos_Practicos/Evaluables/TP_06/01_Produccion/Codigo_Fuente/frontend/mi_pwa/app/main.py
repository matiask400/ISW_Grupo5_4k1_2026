from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI(title="Mi Servidor PWA")

# Ruta absoluta al directorio 'static'
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

# 1. Montar directorio para recursos generales (css, js, imágenes)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# 2. Servir el Service Worker en la raíz o con header Service-Worker-Allowed
# El SW debe controlar el scope deseado; servirlo directamente facilita el registro.
@app.get("/sw.js")
async def get_service_worker():
    return FileResponse(
        STATIC_DIR / "js" / "sw.js", 
        media_type="application/javascript"
    )

# 3. Servir el manifest.json
@app.get("/manifest.json")
async def get_manifest():
    return FileResponse(
        STATIC_DIR / "manifest.json", 
        media_type="application/json"
    )

# 4. Ruta principal para servir la UI (Single Page Application)
@app.get("/")
async def serve_index():
    return FileResponse(STATIC_DIR / "index.html")

# 5. Endpoint de prueba de la API
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "app": "PWA FastAPI"}