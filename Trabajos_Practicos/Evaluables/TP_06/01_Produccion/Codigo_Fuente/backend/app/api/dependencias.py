import os
from datetime import datetime
from functools import lru_cache
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from fastapi import Header, HTTPException

from app.integraciones.email_smtp import ServicioEmailSMTP
from app.integraciones.mercado_pago import PasarelaMercadoPago
from app.repositorios.repositorio_compras import RepositorioComprasEnMemoria
from app.repositorios.repositorio_usuarios import RepositorioUsuariosEnMemoria
from app.servicios.servicio_compra import ServicioCompra

load_dotenv()

ZONA_HORARIA_PARQUE = ZoneInfo("America/Argentina/Cordoba")
USUARIO_DEMO = os.getenv("USUARIO_DEMO", "prueba@gmail.com")


class ConfiguracionFaltanteError(RuntimeError):
    """Falta una variable de entorno obligatoria (ver backend/.env)."""


def _variable_obligatoria(nombre: str) -> str:
    valor = os.getenv(nombre)
    if not valor:
        raise ConfiguracionFaltanteError(f"Falta configurar {nombre} en backend/.env")
    return valor


def _crear_pasarela() -> PasarelaMercadoPago:
    return PasarelaMercadoPago(
        access_token=_variable_obligatoria("MP_ACCESS_TOKEN"),
        url_retorno=os.getenv("URL_RETORNO_PAGO", "http://localhost:5173/compra-finalizada"),
    )


def _crear_servicio_email() -> ServicioEmailSMTP:
    return ServicioEmailSMTP(
        host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
        puerto=int(os.getenv("SMTP_PUERTO", "587")),
        usuario=_variable_obligatoria("SMTP_USUARIO"),
        contrasena=_variable_obligatoria("SMTP_CONTRASENA"),
    )


@lru_cache
def obtener_servicio_compra() -> ServicioCompra:
    return ServicioCompra(
        usuarios=RepositorioUsuariosEnMemoria({USUARIO_DEMO}),
        compras=RepositorioComprasEnMemoria(),
        pasarela=_crear_pasarela(),
        email=_crear_servicio_email(),
        ahora=lambda: datetime.now(ZONA_HORARIA_PARQUE).replace(tzinfo=None),
    )

def obtener_usuario_actual(
    usuario_email: str | None = Header(default=None, alias="X-Usuario-Email"),
) -> str:
    """Sesión simulada (FAQ 19). Con un login real, acá se validaría un token."""
    if not usuario_email:
        raise HTTPException(status_code=401, detail="Debe iniciar sesión")
    return usuario_email
