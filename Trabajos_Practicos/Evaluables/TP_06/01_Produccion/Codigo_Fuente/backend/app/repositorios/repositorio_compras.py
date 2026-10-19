import secrets
import string
from dataclasses import dataclass, field
from datetime import date

from app.modelos.modelos import SolicitudCompra

CARACTERES_CODIGO = string.ascii_uppercase + string.digits


def generar_codigo_entrada() -> str:
    """Código aleatorio que va en el QR del mail, p. ej. EHP-7K2Q9XMA."""
    return "EHP-" + "".join(secrets.choice(CARACTERES_CODIGO) for _ in range(8))


@dataclass
class CompraRegistrada:
    id: str
    solicitud: SolicitudCompra
    monto_total: int
    mail_enviado: bool = False
    codigo_entrada: str = field(default_factory=generar_codigo_entrada)


class RepositorioComprasEnMemoria:
    """Compras registradas, guardadas en memoria."""

    def __init__(self) -> None:
        self._compras: dict[str, CompraRegistrada] = {}

    def guardar(self, compra: CompraRegistrada) -> None:
        self._compras[compra.id] = compra

    def obtener(self, id_compra: str) -> CompraRegistrada | None:
        return self._compras.get(id_compra)

    def entradas_compradas(self, email: str, fecha: date) -> int:
        return sum(
            compra.solicitud.cantidad
            for compra in self._compras.values()
            if compra.solicitud.usuario_email == email and compra.solicitud.fecha_visita == fecha
        )
