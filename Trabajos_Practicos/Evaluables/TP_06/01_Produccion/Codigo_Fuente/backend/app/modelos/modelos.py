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
    def fallida(cls, error: str) -> "ResultadoCompra":
        return cls(exitosa=False, error=error)

    @property
    def mensaje(self) -> str | None:
        if not self.exitosa:
            return None
        palabra = "entrada" if self.cantidad == 1 else "entradas"
        fecha = self.fecha_visita.strftime("%d/%m/%Y")
        return (
            f"Compraste {self.cantidad} {palabra} para el {fecha}. "
            f"Total: ${formatear_pesos(self.monto_total)}"
        )

    url_pago: str | None = None
    mail_enviado_a: str | None = None
    acceso_denegado: bool = False

    @classmethod
    def denegada(cls, error: str) -> "ResultadoCompra":
        return cls(exitosa=False, error=error, acceso_denegado=True)

    @classmethod
    def ok(
        cls,
        cantidad: int,
        fecha_visita: date,
        monto_total: int,
        url_pago: str | None = None,
        mail_enviado_a: str | None = None,
    ) -> "ResultadoCompra":
        return cls(
            exitosa=True,
            cantidad=cantidad,
            fecha_visita=fecha_visita,
            monto_total=monto_total,
            url_pago=url_pago,
            mail_enviado_a=mail_enviado_a,
        )

def formatear_pesos(monto: int) -> str:
    """20000 -> '20.000'"""
    return f"{monto:,}".replace(",", ".")
