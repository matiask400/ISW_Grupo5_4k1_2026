from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencias import obtener_servicio_compra, obtener_usuario_actual
from app.api.esquemas import PedidoCompra, RespuestaCompra
from app.modelos.modelos import SolicitudCompra
from app.servicio.servicio_compra import ServicioCompra

router = APIRouter(prefix="/api/compras", tags=["Compras"])


@router.post("", status_code=201, response_model=RespuestaCompra)
def comprar_entradas(
    pedido: PedidoCompra,
    usuario_email: str = Depends(obtener_usuario_actual),
    servicio: ServicioCompra = Depends(obtener_servicio_compra),
) -> RespuestaCompra:
    solicitud = SolicitudCompra(usuario_email=usuario_email, **pedido.model_dump())
    resultado = servicio.comprar(solicitud)
    if resultado.acceso_denegado:
        raise HTTPException(status_code=403, detail=resultado.error)
    if not resultado.exitosa:
        raise HTTPException(status_code=422, detail=resultado.error)
    return RespuestaCompra.desde_resultado(resultado)
