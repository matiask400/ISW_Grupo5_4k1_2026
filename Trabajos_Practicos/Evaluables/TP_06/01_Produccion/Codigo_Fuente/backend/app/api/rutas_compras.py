from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencias import obtener_servicio_compra, obtener_usuario_actual
from app.api.esquemas import PedidoCompra, PedidoConfirmarPago, RespuestaCompra
from app.modelos.modelos import ResultadoCompra, SolicitudCompra
from app.servicios.servicio_compra import ServicioCompra

router = APIRouter(prefix="/api/compras", tags=["Compras"])


@router.post("", status_code=201, response_model=RespuestaCompra)
def comprar_entradas(
    pedido: PedidoCompra,
    usuario_email: str = Depends(obtener_usuario_actual),
    servicio: ServicioCompra = Depends(obtener_servicio_compra),
) -> RespuestaCompra:
    solicitud = SolicitudCompra(usuario_email=usuario_email, **pedido.model_dump())
    resultado = servicio.comprar(solicitud)
    _rechazar_si_fallo(resultado)
    return RespuestaCompra.desde_resultado(resultado)


@router.post("/confirmar-pago", response_model=RespuestaCompra)
def confirmar_pago(
    pedido: PedidoConfirmarPago,
    usuario_email: str = Depends(obtener_usuario_actual),
    servicio: ServicioCompra = Depends(obtener_servicio_compra),
) -> RespuestaCompra:
    """Lo llama el frontend al volver de Mercado Pago (?payment_id=...)."""
    resultado = servicio.confirmar_pago(pedido.payment_id, usuario_email)
    _rechazar_si_fallo(resultado)
    return RespuestaCompra.desde_resultado(resultado)


def _rechazar_si_fallo(resultado: ResultadoCompra) -> None:
    if resultado.acceso_denegado:
        raise HTTPException(status_code=403, detail=resultado.error)
    if not resultado.exitosa:
        raise HTTPException(status_code=422, detail=resultado.error)
