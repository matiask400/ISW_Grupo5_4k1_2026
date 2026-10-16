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
    tipo_pase: TipoPase | None
    forma_pago: FormaPago | None


@dataclass
class ResultadoCompra:
    exitosa: bool
    error: str | None = None
    cantidad: int | None = None
    fecha_visita: date | None = None
    monto_total: int | None = None

    @classmethod
    def ok(cls, cantidad: int, fecha_visita: date, monto_total: int) -> "ResultadoCompra":
        return cls(
            exitosa=True,
            cantidad=cantidad,
            fecha_visita=fecha_visita,
            monto_total=monto_total,
        )

    @classmethod
    def fallida(cls, error: str) -> "ResultadoCompra":
        return cls(exitosa=False, error=error)
