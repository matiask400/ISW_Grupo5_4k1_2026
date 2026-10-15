from app.modelos.modelos import ResultadoCompra, SolicitudCompra


MAXIMO_ENTRADAS_POR_COMPRA = 10


class ServicioCompra:
    def comprar(self, solicitud: SolicitudCompra) -> ResultadoCompra:
        if solicitud.cantidad < 1:
            return ResultadoCompra.fallida("Debe comprar al menos 1 entrada")
        if solicitud.cantidad > MAXIMO_ENTRADAS_POR_COMPRA:
            return ResultadoCompra.fallida(
                f"La cantidad de entradas no puede superar {MAXIMO_ENTRADAS_POR_COMPRA}"
            )
        if solicitud.forma_pago is None:
            return ResultadoCompra.fallida("Debe seleccionar una forma de pago")
        return ResultadoCompra.ok()
