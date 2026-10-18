from dataclasses import dataclass
from datetime import date

from app.modelos.modelos import SolicitudCompra


@dataclass
class CompraRegistrada:
    id: str
    solicitud: SolicitudCompra
    monto_total: int
    mail_enviado: bool = False


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
