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
    cantidad: int
    fecha_visita: date
    monto_total: int
    url_pago: str | None
    mail_enviado_a: str
    mensaje: str

    @classmethod
    def desde_resultado(cls, resultado: ResultadoCompra) -> "RespuestaCompra":
        return cls(
            cantidad=resultado.cantidad,
            fecha_visita=resultado.fecha_visita,
            monto_total=resultado.monto_total,
            url_pago=resultado.url_pago,
            mail_enviado_a=resultado.mail_enviado_a,
            mensaje=resultado.mensaje,
        )
