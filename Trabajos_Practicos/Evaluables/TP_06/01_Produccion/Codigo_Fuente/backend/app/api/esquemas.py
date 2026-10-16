from datetime import date

from pydantic import BaseModel

from app.modelos.modelos import FormaPago, ResultadoCompra, TipoPase


class PedidoCompra(BaseModel):
    fecha_visita: date
    cantidad: int
    edades: list[int]
    tipo_pase: TipoPase | None = None
    forma_pago: FormaPago | None = None


class RespuestaCompra(BaseModel):
    exitosa: bool
    error: str | None = None
    cantidad: int | None = None
    fecha_visita: date | None = None
    monto_total: int | None = None
    mensaje: str | None = None
    url_pago: str | None = None
    mail_enviado_a: str | None = None

    @classmethod
    def desde_resultado(cls, resultado: ResultadoCompra) -> "RespuestaCompra":
        return cls(
            exitosa=resultado.exitosa,
            error=resultado.error,
            cantidad=resultado.cantidad,
            fecha_visita=resultado.fecha_visita,
            monto_total=resultado.monto_total,
            mensaje=resultado.mensaje,
            url_pago=resultado.url_pago,
            mail_enviado_a=resultado.mail_enviado_a,
        )
