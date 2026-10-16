from datetime import date

from app.modelos.modelos import SolicitudCompra


class RepositorioComprasEnMemoria:
    """Compras registradas, guardadas en memoria."""

    def __init__(self) -> None:
        self._compras: list[SolicitudCompra] = []

    def guardar(self, compra: SolicitudCompra) -> None:
        self._compras.append(compra)

    def entradas_compradas(self, email: str, fecha: date) -> int:
        return sum(
            compra.cantidad
            for compra in self._compras
            if compra.usuario_email == email and compra.fecha_visita == fecha
        )
