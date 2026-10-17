from datetime import datetime
from functools import lru_cache
from zoneinfo import ZoneInfo
from fastapi import Header, HTTPException

from app.integraciones.mercado_pago import PasarelaMercadoPagoSimulada
from app.repositorios.repositorio_compras import RepositorioComprasEnMemoria
from app.repositorios.repositorio_usuarios import RepositorioUsuariosEnMemoria
from app.servicios.servicio_compra import ServicioCompra
from app.integraciones.email import ServicioEmailSimulado

ZONA_HORARIA_PARQUE = ZoneInfo("America/Argentina/Cordoba")
USUARIO_DEMO = "prueba@gmail.com"


@lru_cache
def obtener_servicio_compra() -> ServicioCompra:
    return ServicioCompra(
        usuarios=RepositorioUsuariosEnMemoria({USUARIO_DEMO}),
        compras=RepositorioComprasEnMemoria(),
        pasarela=PasarelaMercadoPagoSimulada(),
        email=ServicioEmailSimulado(),
        ahora=lambda: datetime.now(ZONA_HORARIA_PARQUE).replace(tzinfo=None),
    )

def obtener_usuario_actual(
    usuario_email: str | None = Header(default=None, alias="X-Usuario-Email"),
) -> str:
    """Sesión simulada (FAQ 19). Con un login real, acá se validaría un token."""
    if not usuario_email:
        raise HTTPException(status_code=401, detail="Debe iniciar sesión")
    return usuario_email
