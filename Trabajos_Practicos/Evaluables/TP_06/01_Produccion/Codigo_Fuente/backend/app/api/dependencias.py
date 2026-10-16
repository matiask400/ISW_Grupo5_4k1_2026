from datetime import datetime
from functools import lru_cache
from zoneinfo import ZoneInfo

from app.servicio.pasarela_pago import PasarelaMercadoPagoSimulada
from app.servicio.repositorio_compras import RepositorioComprasEnMemoria
from app.servicio.repositorio_usuarios import RepositorioUsuariosEnMemoria
from app.servicio.servicio_compra import ServicioCompra
from app.servicio.servicio_email import ServicioEmailSimulado

ZONA_HORARIA_PARQUE = ZoneInfo("America/Argentina/Cordoba")
USUARIO_DEMO = "visitante@ecoharmony.com"


@lru_cache
def obtener_servicio_compra() -> ServicioCompra:
    return ServicioCompra(
        usuarios=RepositorioUsuariosEnMemoria({USUARIO_DEMO}),
        compras=RepositorioComprasEnMemoria(),
        pasarela=PasarelaMercadoPagoSimulada(),
        email=ServicioEmailSimulado(),
        ahora=lambda: datetime.now(ZONA_HORARIA_PARQUE).replace(tzinfo=None),
    )
