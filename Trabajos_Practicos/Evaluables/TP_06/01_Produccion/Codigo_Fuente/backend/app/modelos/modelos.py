from dataclasses import dataclass
from datetime import date
from enum import Enum


class TipoPase(Enum):
    REGULAR = "REGULAR"
    VIP = "VIP"


class FormaPago(Enum):
    EFECTIVO = "EFECTIVO"
    TARJETA = "TARJETA"


@dataclass
class SolicitudCompra:
    usuario_email: str
    fecha_visita: date
    cantidad: int
    edades: list[int]
    tipo_pase: TipoPase
    forma_pago: FormaPago


@dataclass
class ResultadoCompra:
    exitosa: bool
    error: str | None = None

    @classmethod
    def ok(cls) -> "ResultadoCompra":
        return cls(exitosa=True)

    @classmethod
    def fallida(cls, error: str) -> "ResultadoCompra":
        return cls(exitosa=False, error=error)